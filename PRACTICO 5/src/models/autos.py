from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.marcas import Marca


class Auto(SQLModel, table=True):
    __tablename__ = "autos"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    marca_id: int = Field(foreign_key="marcas.id", nullable=False, index=True)
    modelo: str = Field(min_length=1, max_length=30)
    anio: int = Field(ge=1900, le=2100)
    precio: float = Field(gt=0)

    # Relación muchos a uno con Marca
    marca: Optional["Marca"] = Relationship(back_populates="autos")
