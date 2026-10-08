from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from database import get_db
from models.marcas import Marca
from schemas.marcas import MarcaCreate, MarcaRead, MarcaReadWithAutos

router = APIRouter()


@router.post("/", response_model=MarcaRead, status_code=status.HTTP_201_CREATED)
def crear_marca(marca: MarcaCreate, db: Session = Depends(get_db)):
    marca_existente = db.exec(select(Marca).where(Marca.nombre == marca.nombre)).first()
    if marca_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una marca registrada con el nombre '{marca.nombre}'"
        )

    nueva_marca = Marca.model_validate(marca)
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    return nueva_marca


@router.get("/", response_model=list[MarcaRead])
def obtener_marcas(db: Session = Depends(get_db)):
    return db.exec(select(Marca)).all()


@router.get(
    "/{id_marca}",
    response_model=MarcaReadWithAutos,
    responses={404: {"description": "Marca no encontrada"}}
)
def obtener_marca(
    id_marca: Annotated[int, Path(gt=0, description="ID de la marca")],
    db: Session = Depends(get_db)
):
    marca = db.get(Marca, id_marca)
    if marca is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marca no encontrada"
        )
    return marca
