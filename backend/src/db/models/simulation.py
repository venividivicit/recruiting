from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


class Simulation(Base):
    __tablename__ = "simulations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data: Mapped[str] = mapped_column(Text, nullable=False)