from app.definitions.exceptions import AppException
from app.utils import IDEnum
from tests.base_test_case import BaseTestCase


class TestDistributorRepository(BaseTestCase):
    distributor_data = {
        "phone_number": "00233242583061",
        "first_name": "John",
        "last_name": "Doe",
        "id_type": "passport",
        "id_number": "4829h9445839",
        "auth_service_id": "d9247e56-7ad4-434d-8524-606e69d784c3",
    }

    def test_create(self):
        distributor = self.distributor_repository.create(self.distributor_data)
        self.assertEqual(distributor.first_name, "John")

    def test_update(self):
        distributor = self.distributor_repository.create(self.distributor_data)

        self.assertEqual(distributor.first_name, "John")

        updated_distributor = self.distributor_repository.update_by_id(
            distributor.id, {"first_name": "Joe"}
        )

        self.assertEqual(updated_distributor.first_name, "Joe")

    def test_delete(self):
        distributor = self.distributor_repository.create(self.distributor_data)
        distributor_search = self.distributor_repository.find_by_id(distributor.id)

        self.assertEqual(distributor_search.id, distributor.id)
        self.assertEqual(distributor_search.id_type, IDEnum.passport)

        self.distributor_repository.delete(distributor.id)

        with self.assertRaises(AppException.NotFoundException):
            self.distributor_repository.find_by_id(distributor.id)

    def test_required_fields(self):
        distributor_data = {
            "last_name": "Doe",
            "id_type": "passport",
            "id_number": "4829h9445839",
        }

        with self.assertRaises(AppException.OperationError):
            self.distributor_repository.create(distributor_data)

    def test_duplicates(self):
        self.distributor_repository.create(self.distributor_data)

        with self.assertRaises(AppException.OperationError):
            self.distributor_repository.create(self.distributor_data)
