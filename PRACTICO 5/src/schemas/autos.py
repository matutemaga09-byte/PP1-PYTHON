from typing import Optional
from sqlmodel import Field, SQLModel

from schemas.marcas import MarcaRead, MarcaReadWithAutos


class AutoBase(SQLModel):
    marca_id: int = Field(gt=0, description="ID de la marca a la que pertenece el auto")
    modelo: str = Field(min_length=1, max_length=30, description="Modelo del vehículo")
    anio: int = Field(ge=1900, le=2100, description="Año del vehículo")
    precio: float = Field(gt=0, description="Precio del vehículo")


class AutoCreate(AutoBase):
    pass


class AutoUpdate(SQLModel):
    marca_id: Optional[int] = Field(default=None, gt=0, description="ID de la marca")
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=30, description="Modelo")
    anio: Optional[int] = Field(default=None, ge=1900, le=2100, description="Año del vehículo")
    precio: Optional[float] = Field(default=None, gt=0, description="Precio del vehículo")


class AutoRead(AutoBase):
    id: int = Field(gt=0, description="Identificador único del auto")


class AutoReadWithMarca(AutoRead):
    marca: Optional[MarcaRead] = None


# Reconstruir schemas con referencias diferidas para soportar anidamiento
MarcaReadWithAutos.model_rebuild(_types_namespace={"AutoRead": AutoRead})
AutoReadWithMarca.model_rebuild()

# Alias de conveniencia para retrocompatibilidad
Auto = AutoReadWithMarca
