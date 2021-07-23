import random
import secrets
import pytz
from datetime import datetime, timedelta

from app.definitions import Result, ServiceResult
from app.definitions.exceptions import AppException
from app.definitions.notifier import Notifier
from app.definitions.service_interfaces import AuthServiceInterface
from app.repositories import DistributorRepository, LeadRepository
from app.notifications import SMSNotificationHandler


utc = pytz.UTC


class DistributorController(Notifier):
    def __init__(
        self,
        distributor_repository: DistributorRepository,
        lead_repository: LeadRepository,
        auth_service: AuthServiceInterface,
    ):
        self.lead_repository = lead_repository
        self.distributor_repository = distributor_repository
        self.auth_service = auth_service

    def register(self, data):

        phone_number = data.get("phone_number")
        existing_distributor = self.distributor_repository.find({"phone_number": phone_number})

        if existing_distributor:
            raise AppException.ResourceExists(
                f"Distributor with phone number {phone_number} exists"
            )

        otp = random.randint(100000, 999999)
        otp_expiration = datetime.now() + timedelta(minutes=5)

        data["otp"] = otp
        data["otp_expiration"] = otp_expiration

        distributor = self.lead_repository.create(data)

        self.notify(
            SMSNotificationHandler(distributor.phone_number, {"otp": otp}, "sms_otp")
        )

        return ServiceResult(Result({"id": distributor.id}, 201))

    def confirm_token(self, data):
        uuid = data.get("id")
        otp = data.get("token")
        lead = self.lead_repository.find({"id": uuid, "otp": otp})
        if not lead:
            raise AppException.BadRequest("Invalid authentication token")

        if utc.localize(dt=datetime.now()) > lead.otp_expiration:
            raise AppException.ExpiredTokenException("token expired")

        password_token = secrets.token_urlsafe(16)

        updated_lead = self.lead_repository.update_by_id(
            lead.id,
            {
                "password_token": password_token,
                "password_token_expiration": datetime.now() + timedelta(minutes=3),
            },
        )

        token_data = {"password_token": updated_lead.password_token}
        return ServiceResult(Result(token_data, 200))

    def resend_token(self, lead_id):
        lead = self.lead_repository.find_by_id(lead_id)
        otp = random.randint(100000, 999999)
        otp_expiration = datetime.now() + timedelta(minutes=5)

        updated_lead = self.lead_repository.update_by_id(
            lead_id, {"otp": otp, "otp_expiration": otp_expiration}
        )

        self.notify(SMSNotificationHandler(lead.phone_number, {"otp": otp}, "sms_otp"))
        return ServiceResult(Result({"id": updated_lead.id}, 201))

    def add_pin(self, data):
        token = data.get("password_token")
        pin = data.get("pin")

        # find if password_token exists
        user = self.lead_repository.find({"password_token": token})

        if not user:
            raise AppException.NotFoundException("User does not exist")

        # Check if password_token is valid or expired
        if utc.localize(dt=datetime.now()) > user.password_token_expiration:
            raise AppException.ExpiredTokenException("token expired")

        user_data = {
            "username": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": pin,
        }
        # Create user in auth service
        auth_result = self.auth_service.create_user(user_data)

        # Create user in Distributor table
        distributor_data = {
            "id": user.id,
            "phone_number": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "id_type": user.id_type,
            "id_number": user.id_number,
            "status": "active",
            "auth_service_id": auth_result.get("id"),
        }

        self.distributor_repository.create(distributor_data)
        # Remove id from auth_result
        auth_result.pop("id", None)
        return ServiceResult(Result(auth_result, 200))

    def find_distributor_by_phone(self, phone_number):
        assert phone_number, "Missing phone number"
        distributor = self.distributor_repository.find({"phone_number": phone_number})
        return distributor

    def login(self, data):
        phone_number = data.get("phone_number")
        pin = data.get("pin")
        distributor = self.distributor_repository.find({"phone_number": phone_number})
        if not Distributor:
            raise AppException.NotFoundException("User does not exist")

        access_token = self.auth_service.get_token(
            {"username": distributor.id, "password": pin}
        )

        return ServiceResult(Result(access_token, 200))

    def show(self, distributor_id):
        distributor = self.distributor_repository.find_by_id(distributor_id)
        result = ServiceResult(Result(distributor, 200))
        return result

    def update(self, distributor_id, data):
        distributor = self.distributor_repository.update_by_id(distributor_id, data)
        result = ServiceResult(Result(distributor, 200))
        return result

    def delete(self, distributor_id):
        self.distributor_repository.delete(distributor_id)
        result = ServiceResult(Result({}, 204))
        return result
