import os
from flask_testing import TestCase
from app import create_app, db
from app.controllers import DistributorController
from app.repositories import DistributorRepository, LeadRepository
from tests import MockAuthService


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="sqlite:///"
            + os.path.join(app.instance_path, "test.db?check_same_thread=False"),
        )
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
        self.distributor_repository = DistributorRepository()
        self.lead_repository = LeadRepository()
        self.auth_service = MockAuthService()
        self.distributor_controller = DistributorController(
            distributor_repository=self.distributor_repository,
            auth_service=self.auth_service,
            lead_repository=self.lead_repository,
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

        path = self.app.instance_path
        file = os.path.join(path, "test.db")
        os.remove(file)

    def dummy_kafka_method(self, topic, value):
        return True
