import json
from sqlalchemy.orm import Session
from src.db.repositories.simulation_repo import SimulationRepository
from src.domain.store import QRangeStore
from src.domain.simulator import Simulator


class SimulationService:
    def __init__(self, db: Session):
        self.repo = SimulationRepository(db)

    def get_latest(self):
        latest = self.repo.get_latest()
        return json.loads(latest.data) if latest else []

    def run(self, init: dict):
        # preserve old behavior
        for key in init.keys():
            init[key]["time"] = 0
            init[key]["timeStep"] = 0.01

        store = QRangeStore()
        simulator = Simulator(store=store, init=init)
        simulator.simulate()

        self.repo.create(json.dumps(store.store))
        return store.store