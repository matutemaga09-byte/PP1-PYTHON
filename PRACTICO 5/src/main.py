import os
import sys

# Asegurar que el directorio 'src' esté en sys.path para soportar ejecución
# tanto desde la raíz del proyecto (uvicorn src.main:app) como desde src/ (uvicorn main:app)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.autos import router as autos_router
from routers.marcas import router as marcas_router

app = FastAPI(
    title="Concesionaria de Autos API",
    description="API REST desarrollada con FastAPI, SQLModel y Alembic para la gestión de concesionaria de autos.",
    version="2.0.0"
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    marcas_router,
    prefix="/marcas",
    tags=["Marcas"]
)

app.include_router(
    autos_router,
    prefix="/autos",
    tags=["Autos"]
)


@app.get("/", tags=["General"])
def read_root():
    return {
        "mensaje": "API de Concesionaria en funcionamiento",
        "documentacion": "/docs",
        "redoc": "/redoc"
    }
