# Práctico 5 — Concesionaria de Autos API (SQLModel + Alembic)

Evolución del **Práctico 4** adaptada para implementar **SQLModel** como ORM principal y **Alembic** para la gestión y ejecución de migraciones sobre base de datos SQLite.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+ / 3.14**
- **FastAPI**: Framework web para la construcción de la API REST.
- **SQLModel**: Modelado ORM y schemas de validación de datos (basado en SQLAlchemy y Pydantic).
- **Alembic**: Sistema de control de versiones y migraciones de la base de datos.
- **SQLite**: Motor de base de datos relacional en archivo local.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.

---

## 📁 Estructura del Proyecto

```text
PRACTICO 5/
│
├── alembic.ini                   # Configuración principal de Alembic
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Documentación de uso y entrega
├── .gitignore                    # Reglas de exclusión para Git
├── seed.py                       # Script opcional para cargar datos iniciales
│
├── alembic/                      # Directorio de control de migraciones
│   ├── env.py                    # Configuración del entorno de migraciones con SQLModel.metadata
│   ├── script.py.mako            # Plantilla para generación de scripts de migración
│   └── versions/
│       └── 9552472da095_crear_tablas_iniciales_marcas_y_autos.py # Migración inicial
│
└── src/                          # Código fuente de la aplicación
    ├── concesionaria.db          # Base de datos SQLite generada por Alembic
    ├── database.py               # Configuración del motor SQLModel y dependencia de sesión
    ├── main.py                   # Instancia FastAPI y registro de routers
    │
    ├── models/                   # Modelos de tabla SQLModel (ORM)
    │   ├── __init__.py           # Registro de modelos en SQLModel.metadata
    │   ├── marcas.py             # Modelo de tabla 'marcas' y relación 1:N
    │   └── autos.py              # Modelo de tabla 'autos' y clave foránea (marca_id)
    │
    ├── schemas/                  # Schemas SQLModel para validación y datos anidados
    │   ├── marcas.py             # Schemas Marca (Base, Create, Update, Read, ReadWithAutos)
    │   └── autos.py              # Schemas Auto (Base, Create, Update, Read, ReadWithMarca)
    │
    └── routers/                  # Endpoints de la API
        ├── marcas.py             # CRUD y consultas de marcas
        └── autos.py              # CRUD de autos con serialización anidada
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio y crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar las migraciones de Alembic

Alembic se encargará de crear las tablas `marcas` y `autos` (junto con sus claves foráneas e índices) sin necesidad de `create_all()`:

```bash
alembic upgrade head
```

### 4. (Opcional) Cargar datos de prueba

Para insertar marcas iniciales (Ford, Fiat, Toyota) y autos de ejemplo:

```bash
python seed.py
```

### 5. Iniciar la API con FastAPI y Uvicorn

```bash
uvicorn src.main:app --reload
```

La API quedará accesible en:
- **API Base:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Documentación Swagger UI interactiva:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Documentación ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Endpoints Principales

### 🏷️ Marcas (`/marcas`)

| Método | Endpoint | Descripción | Body / Parámetros |
| :--- | :--- | :--- | :--- |
| `POST` | `/marcas/` | Crear una nueva marca | `{"nombre": "Toyota"}` |
| `GET` | `/marcas/` | Listar todas las marcas | - |
| `GET` | `/marcas/{id_marca}` | Obtener marca por ID con sus autos anidados | `id_marca: int` |

### 🚗 Autos (`/autos`)

| Método | Endpoint | Descripción | Body / Parámetros |
| :--- | :--- | :--- | :--- |
| `POST` | `/autos/` | Crear un auto (asociado a `marca_id`) | `{"marca_id": 1, "modelo": "Corolla", "anio": 2024, "precio": 25000}` |
| `GET` | `/autos/` | Listar todos los autos con marca anidada | - |
| `GET` | `/autos/{id_auto}` | Obtener auto por ID con marca anidada | `id_auto: int` |
| `PUT` | `/autos/{id_auto}` | Actualizar datos de un auto | `{"modelo": "Corolla Cross", "precio": 32000}` |
| `DELETE` | `/autos/{id_auto}` | Eliminar un auto por ID | `id_auto: int` |

---

## 🔍 Demostración de Datos Anidados

Al consultar un auto (`GET /autos/1`), la respuesta devuelve la marca anidada:

```json
{
  "id": 1,
  "marca_id": 1,
  "modelo": "Corolla",
  "anio": 2024,
  "precio": 25000.0,
  "marca": {
    "id": 1,
    "nombre": "Toyota"
  }
}
```

De manera inversa, al consultar una marca (`GET /marcas/1`), devuelve los autos asociados:

```json
{
  "id": 1,
  "nombre": "Toyota",
  "autos": [
    {
      "id": 1,
      "marca_id": 1,
      "modelo": "Corolla",
      "anio": 2024,
      "precio": 25000.0
    }
  ]
}
```
