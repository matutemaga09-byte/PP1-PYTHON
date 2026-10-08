from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.autos import Auto


class Marca(SQLModel, table=True):
    __tablename__ = "marcas"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, min_length=2, max_length=50)

    # Relación uno a muchos con Auto
    autos: list["Auto"] = Relationship(back_populates="marca", cascade_delete=True)
