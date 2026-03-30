from pydantic import BaseModel, ConfigDict, Field, model_validator


class Vector3(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: float
    y: float
    z: float


class BodyState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position: Vector3
    velocity: Vector3
    mass: float = Field(gt=0)


class SimulationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    init: dict[str, BodyState]

    @model_validator(mode="after")
    def validate_agents(self):
        if not self.init:
            raise ValueError("init must include at least one agent")
        return self