from pathlib import Path
from sqlmodel import Session, create_engine

# Database.py
# Gestión de la conexión a la DB -> Usando SQLModel

# Ruta hacia la base de datos SQLite dentro de src/
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "concesionaria.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Motor de conexión con SQLModel
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def get_db():
    with Session(engine) as session:
        yield session
