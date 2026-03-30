from typing import Any
from pydantic import BaseModel


class SimulationCreate(BaseModel):
    init: dict[str, dict[str, Any]]