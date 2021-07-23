from app.definitions.exceptions import AppException
from app.utils import IDEnum
from tests.base_test_case import BaseTestCase


class TestDistributorController(BaseTestCase):
    customer_data = {
        "phone_number": "00233242583061",
        "first_name": "John",
        "last_name": "Doe",
        "id_type": "passport",
        "id_number": "4829h9445839",
        "auth_service_id": "d9247e56-7ad4-434d-8524-606e69d784c3",
    }

    def test_edit_distributor(self):
        distributor = self.distributor_repository.create(self.customer_data)

        updated_distributor = self.distributor_controller.update(
            distributor.id,
            {
                "first_name": "Jane",
                "last_name": "Dew",
            },
        )

        updated_data = updated_distributor.data.value

        self.assertEqual(updated_data.id, distributor.id)
        self.assertEqual(updated_data.last_name, "Dew")
        self.assertEqual(updated_data.first_name, "Jane")

        distributor_search = self.distributor_repository.find_by_id(updated_data.id)

        self.assertEqual(distributor_search.id, updated_data.id)
        self.assertEqual(distributor_search.last_name, "Dew")

    def test_delete_distributor(self):
        distributor = self.distributor_repository.create(self.distributor_data)

        self.distributor_controller.delete(distributor.id)

        with self.assertRaises(AppException.NotFoundException):
            self.customer_repository.find_by_id(distributor.id)

    def test_show_distributor(self):
        distributor = self.distributor_repository.create(self.distributor_data)
        distributor_search = self.distributor_controller.show(distributor.id)

        distributor_values = distributor_search.data.value
        self.assertEqual(distributor_values.id, distributor.id)
        self.assertEqual(distributor_values.last_name, "Doe")
        self.assertEqual(distributor_values.id_type, IDEnum.passport)
