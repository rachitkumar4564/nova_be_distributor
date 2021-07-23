from app.definitions.repository import SQLBaseRepository
from app.models import Distributor


class DistributorRepository(SQLBaseRepository):
    model = Distributor
