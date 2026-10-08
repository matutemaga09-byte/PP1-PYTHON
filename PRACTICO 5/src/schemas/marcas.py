from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from schemas.autos import AutoRead


class MarcaBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=50, description="Nombre de la marca")


class MarcaCreate(MarcaBase):
    pass


class MarcaUpdate(SQLModel):
    nombre: Optional[str] = Field(
        default=None, min_length=2, max_length=50, description="Nombre de la marca"
    )


class MarcaRead(MarcaBase):
    id: int = Field(gt=0, description="Identificador único de la marca")


class MarcaReadWithAutos(MarcaRead):
    autos: list["AutoRead"] = []
