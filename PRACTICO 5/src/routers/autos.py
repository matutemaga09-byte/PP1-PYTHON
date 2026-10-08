from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from database import get_db
from models.autos import Auto
from models.marcas import Marca
from schemas.autos import AutoCreate, AutoReadWithMarca, AutoUpdate

router = APIRouter()


@router.post("/", response_model=AutoReadWithMarca, status_code=status.HTTP_201_CREATED)
def crear_auto(auto: AutoCreate, db: Session = Depends(get_db)):
    marca = db.get(Marca, auto.marca_id)
    if marca is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Marca con ID {auto.marca_id} no encontrada"
        )

    nuevo = Auto.model_validate(auto)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=list[AutoReadWithMarca])
def obtener_autos(db: Session = Depends(get_db)):
    autos = db.exec(select(Auto)).all()
    return autos


@router.get(
    "/{id_auto}",
    response_model=AutoReadWithMarca,
    responses={404: {"description": "Auto no encontrado"}}
)
def obtener_auto(
    id_auto: Annotated[int, Path(gt=0, description="ID del auto")],
    db: Session = Depends(get_db)
):
    auto = db.get(Auto, id_auto)
    if auto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auto no encontrado"
        )
    return auto


@router.put(
    "/{id_auto}",
    response_model=AutoReadWithMarca,
    responses={404: {"description": "Auto no encontrado"}}
)
def editar_auto(
    id_auto: Annotated[int, Path(gt=0, description="ID del auto")],
    auto_actualizado: AutoUpdate,
    db: Session = Depends(get_db)
):
    auto_db = db.get(Auto, id_auto)
    if auto_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auto no encontrado"
        )

    datos = auto_actualizado.model_dump(exclude_unset=True)

    if "marca_id" in datos and datos["marca_id"] is not None:
        marca = db.get(Marca, datos["marca_id"])
        if marca is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marca con ID {datos['marca_id']} no encontrada"
            )

    for campo, valor in datos.items():
        setattr(auto_db, campo, valor)

    db.add(auto_db)
    db.commit()
    db.refresh(auto_db)
    return auto_db


@router.delete(
    "/{id_auto}",
    response_model=AutoReadWithMarca,
    responses={404: {"description": "Auto no encontrado"}}
)
def eliminar_auto(
    id_auto: Annotated[int, Path(gt=0, description="ID del auto")],
    db: Session = Depends(get_db)
):
    auto = db.get(Auto, id_auto)
    if auto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auto no encontrado"
        )

    auto_eliminado = AutoReadWithMarca.model_validate(auto)

    db.delete(auto)
    db.commit()
    return auto_eliminado
