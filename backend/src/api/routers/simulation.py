from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.schemas.simulation import SimulationCreate
from src.services.simulation_service import SimulationService

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.get("")
def get_latest_simulation(db: Session = Depends(get_db)):
    return SimulationService(db).get_latest()


@router.post("")
def run_simulation(payload: SimulationCreate, db: Session = Depends(get_db)):
    return SimulationService(db).run(payload.init)