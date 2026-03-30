from sqlalchemy.orm import Session
from src.db.models.simulation import Simulation


class SimulationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_latest(self) -> Simulation | None:
        return self.db.query(Simulation).order_by(Simulation.id.desc()).first()

    def create(self, data_json: str) -> Simulation:
        row = Simulation(data=data_json)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row