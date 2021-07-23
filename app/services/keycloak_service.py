import os
import requests
from app.definitions.exceptions.app_exceptions import AppException
from app.definitions.service_interfaces.auth_service_interface import (
    AuthServiceInterface,
)

CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
URI = os.getenv("KEYCLOAK_URI")
REALM = os.getenv("KEYCLOAK_REALM")
REALM_PREFIX = "/auth/realms/"
AUTH_ENDPOINT = "/protocol/openid-connect/token/"


class AuthService(AuthServiceInterface):
    headers = None

    def get_token(self, request_data):
        """
        Login to keycloak and return token
        :param request_data: {dict} a dictionary containing username and password
        :return: {dict} a dictionary containing token and refresh token
        """
        data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": request_data.get("username"),
            "password": request_data.get("password"),
        }

        # create keycloak uri for token login
        url = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT

        response = requests.post(url, data=data)

        # handle error if its anything more than a 200 as a 200 response is the
        # only expected response
        if response.status_code != 200:
            raise AppException.KeyCloakAdminException(
                context={"message": "Error in username or password"},
                status_code=response.status_code,
            )

        tokens_data = response.json()
        result = {
            "access_token": tokens_data["access_token"],
            "refresh_token": tokens_data["refresh_token"],
        }

        return result

    def refresh_token(self, refresh_token):
        """

        :param refresh_token: a {str} containing the refresh token
        :return: {dict} a dictionary containing the token and refresh token
        """
        request_data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        }

        url = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT

        response = requests.post(url, data=request_data)

        if response.status_code != requests.codes.ok:
            raise AppException.BadRequest(
                context={"errorMessage": "Error in refresh token"}
            )

        data = response.json()
        return {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
        }

    def create_user(self, request_data):
        data = {
            "email": request_data.get("email"),
            "username": request_data.get("username"),
            "firstName": request_data.get("first_name"),
            "lastName": request_data.get("last_name"),
            "credentials": [
                {
                    "value": request_data.get("password"),
                    "type": "password",
                    "temporary": False,
                }
            ],
            "enabled": True,
            "emailVerified": True,
            "access": {
                "manageGroupMembership": True,
                "view": True,
                "mapRoles": True,
                "impersonate": True,
                "manage": True,
            },
        }

        endpoint = "/users"
        # create user
        self.keycloak_post(endpoint, data)

        # get user details from keycloak
        user = self.get_keycloak_user(request_data.get("username"))
        user_id = user.get("id")

        # assign keycloak role
        self.assign_role(user_id)

        # login user and return token
        token_data = self.get_token(
            {
                "username": request_data.get("username"),
                "password": request_data.get("password"),
            }
        )
        token_data["id"] = user_id
        return token_data

    def get_keycloak_user(self, username):
        url = URI + "/auth/admin/realms/" + REALM + "/users?username=" + username
        response = requests.get(url, headers=self.headers or self.get_keycloak_headers())
        if response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                context={"message": response.json().get("errorMessage")},
                status_code=response.status_code,
            )
        user = response.json()
        if len(user) == 0:
            return None
        else:
            return user[0]

    def assign_role(self, user_id):
        url = "/users/" + user_id + "/role-mappings/realm"
        data = [
            {
                "id": "7735d317-c224-4c97-978d-47cc4aaa2ac6",
                "name": "customer",
            }
        ]
        self.keycloak_post(url, data)

    def keycloak_post(self, endpoint, data):
        """
        Make a POST request to Keycloak
        :param {string} endpoint Keycloak endpoint
        :data {object} data Keycloak data object
        :return {Response} request response object
        """
        url = URI + "/auth/admin/realms/" + REALM + endpoint
        headers = self.headers or self.get_keycloak_headers()
        response = requests.post(url, headers=headers, json=data)
        if response.status_code >= 300:
            raise AppException.KeyCloakAdminException(
                context={"message": response.json().get("errorMessage")},
                status_code=response.status_code,
            )
        return response

    # noinspection PyMethodMayBeStatic
    def get_keycloak_access_token(self):
        """
        :returns {string} Keycloak admin user access_token
        """
        data = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": os.getenv("KEYCLOAK_ADMIN_USER"),
            "password": os.getenv("KEYCLOAK_ADMIN_PASSWORD"),
        }

        url = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT

        response = requests.post(
            url,
            data=data,
        )
        if response.status_code != requests.codes.ok:
            raise AppException.KeyCloakAdminException(
                context={"response": response.text}, status_code=500
            )
        data = response.json()
        return data.get("access_token")

    def get_keycloak_headers(self):
        """

        :return {object}  Object of keycloak headers
        """
        headers = {
            "Authorization": "Bearer " + self.get_keycloak_access_token(),
            "Content-Type": "application/json",
        }
        self.headers = headers
        return headers
