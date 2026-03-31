import asyncio
import json
import os
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy.orm import Session

from src.db.repositories.simulation_repo import SimulationRepository
from src.domain.simulator import Simulator
from src.domain.store import QRangeStore

_SIMULATION_PROCESS_POOL = ProcessPoolExecutor(max_workers=os.cpu_count() or 1)


def _normalize_init_payload(init: dict) -> dict:
    init_dict = {
        agent_id: state.model_dump() if hasattr(state, "model_dump") else state
        for agent_id, state in init.items()
    }

    for key in init_dict.keys():
        init_dict[key]["time"] = 0
        init_dict[key]["timeStep"] = 0.01

    return init_dict


def _run_simulation(init_dict: dict):
    store = QRangeStore()
    simulator = Simulator(store=store, init=init_dict)
    simulator.simulate()
    return store.export()


class SimulationService:
    def __init__(self, db: Session):
        self.repo = SimulationRepository(db)

    def get_latest(self):
        latest = self.repo.get_latest()
        return json.loads(latest.data) if latest else []

    def run(self, init: dict):
        init_dict = _normalize_init_payload(init)
        payload = _run_simulation(init_dict)
        self.repo.create(json.dumps(payload))
        return payload

    async def run_async(self, init: dict):
        init_dict = _normalize_init_payload(init)
        loop = asyncio.get_running_loop()
        payload = await loop.run_in_executor(
            _SIMULATION_PROCESS_POOL,
            _run_simulation,
            init_dict,
        )
        self.repo.create(json.dumps(payload))
        return payload