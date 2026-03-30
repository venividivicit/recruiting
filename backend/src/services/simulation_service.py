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
        # Convert Pydantic BodyState objects -> plain dicts
        init_dict = {
            agent_id: state.model_dump() if hasattr(state, "model_dump") else state
            for agent_id, state in init.items()
        }

        # preserve old behavior
        for key in init_dict.keys():
            init_dict[key]["time"] = 0
            init_dict[key]["timeStep"] = 0.01

        store = QRangeStore()
        simulator = Simulator(store=store, init=init_dict)
        simulator.simulate()

        self.repo.create(json.dumps(store.store))
        return store.store