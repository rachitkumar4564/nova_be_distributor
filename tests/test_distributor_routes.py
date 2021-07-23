from unittest import mock
from app.definitions.exceptions import AppException
from tests.base_test_case import BaseTestCase


class TestDistributorRoutes(BaseTestCase):
    distributor_data = {
        "phone_number": "00233242583061",
        "first_name": "John",
        "last_name": "Doe",
        "id_type": "passport",
        "id_number": "4829h9445839",
        "auth_service_id": "d9247e56-7ad4-434d-8524-606e69d784c3",
    }

    account_creation_data = {
        "first_name": "John",
        "last_name": "Doe",
        "id_type": "passport",
        "id_number": "4829h9445839",
        "phone_number": "0242583061",
    }

    @mock.patch("app.notifications.sms_notification_handler.publish_to_kafka")
    def test_create_route(self, kafka_producer_mock):
        kafka_producer_mock.side_effect = self.dummy_kafka_method

        with self.client:
            distributor = self.client.post(
                "/api/v1/distributors/accounts/", json=self.account_creation_data
            )
            self.assertStatus(distributor, 201)

    def test_create_route_error(self):
        with self.client:
            distributor = self.client.post("/api/v1/distributors/accounts/", json={})
            self.assertStatus(distributor, 400)

    def test_update_route(self):
        distributor = self.distributor_repository.create(self.distributor_data)
        self.assertEqual(distributor.phone_number, self.distributor_data["phone_number"])
        with self.client:
            distributor_update = self.client.patch(
                f"/api/v1/distributors/accounts/{distributor.id}", json={"first_name": "Jane"}
            )

            self.assert200(distributor_update)

        distributor_search = self.distributor_repository.find_by_id(distributor.id)
        self.assertEqual(distributor_search.first_name, "Jane")

    def test_delete_route(self):
        distributor = self.distributor_repository.create(self.distributor_data)
        self.assertEqual(distributor.phone_number, self.distributor_data["phone_number"])

        with self.client:
            response = self.client.delete(f"/api/v1/distributors/accounts/{distributor.id}")
            self.assertStatus(response, 204)

        with self.assertRaises(AppException.NotFoundException):
            self.distributor_repository.find_by_id(distributor.id)

    def test_show_route(self):
        distributor = self.distributor_repository.create(self.distributor_data)
        self.assertEqual(distributor.phone_number, self.distributor_data["phone_number"])

        with self.client:
            response = self.client.get(f"/api/v1/distributors/accounts/{distributor.id}")
            self.assertStatus(response, 200)
            data = response.json

            self.assertEqual(
                data.get("first_name"), self.distributor_data.get("first_name")
            )
