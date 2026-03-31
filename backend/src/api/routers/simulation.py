from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.logging_config import get_logger
from src.schemas.simulation import SimulationCreate
from src.services.simulation_service import SimulationService

router = APIRouter(prefix="/simulation", tags=["simulation"])
log = get_logger(__name__)


@router.get("")
def get_latest_simulation(db: Session = Depends(get_db)):
    log.debug("GET /simulation — fetching latest run")
    return SimulationService(db).get_latest()


@router.post("")
async def run_simulation(payload: SimulationCreate, db: Session = Depends(get_db)):
    log.info(
        "POST /simulation — starting run (%d agent(s))",
        len(payload.root),
    )
    return await SimulationService(db).run_async(payload.root)