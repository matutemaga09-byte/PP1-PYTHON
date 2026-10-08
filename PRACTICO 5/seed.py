import sys
import os

# Asegurar que 'src' esté en sys.path
sys.path.insert(0, os.path.abspath("src"))

from sqlmodel import Session, select
from database import engine
from models.marcas import Marca
from models.autos import Auto


def cargar_datos_semilla():
    print("Cargando datos iniciales...")
    with Session(engine) as session:
        # Verificar si ya existen marcas
        marcas_existentes = session.exec(select(Marca)).all()
        if marcas_existentes:
            print("La base de datos ya contiene registros. Omitiendo seed.")
            return

        # Marcas iniciales
        ford = Marca(nombre="Ford")
        fiat = Marca(nombre="Fiat")
        toyota = Marca(nombre="Toyota")

        session.add_all([ford, fiat, toyota])
        session.commit()
        session.refresh(ford)
        session.refresh(fiat)
        session.refresh(toyota)

        # Autos iniciales (equivalentes a los del Práctico 4)
        auto1 = Auto(
            marca_id=ford.id,
            modelo="Focus",
            anio=2015,
            precio=15000000.0
        )
        auto2 = Auto(
            marca_id=fiat.id,
            modelo="Mobi",
            anio=2021,
            precio=10000000.0
        )
        auto3 = Auto(
            marca_id=toyota.id,
            modelo="Corolla",
            anio=2024,
            precio=25000000.0
        )

        session.add_all([auto1, auto2, auto3])
        session.commit()
        print("¡Datos iniciales cargados con éxito!")
        print(f"Marcas: Ford (ID: {ford.id}), Fiat (ID: {fiat.id}), Toyota (ID: {toyota.id})")
        print(f"Autos: Focus, Mobi, Corolla")


if __name__ == "__main__":
    cargar_datos_semilla()
