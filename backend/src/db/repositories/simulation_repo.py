from sqlalchemy.orm import Session

from src.core.logging_config import get_logger
from src.db.models.simulation import Simulation

log = get_logger(__name__)


class SimulationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_latest(self) -> Simulation | None:
        row = self.db.query(Simulation).order_by(Simulation.id.desc()).first()
        log.debug("Repository get_latest -> %s", f"id={row.id}" if row else "none")
        return row

    def create(self, data_json: str) -> Simulation:
        row = Simulation(data=data_json)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        log.debug(
            "Repository create simulation id=%s (payload ~%d bytes)",
            row.id,
            len(data_json),
        )
        return row