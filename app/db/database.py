import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Cargar las variables definidas en el archivo .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "alicia_db")

# 2. Construir la cadena de conexión (Connection String) usando el driver PyMySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. El Engine: Es el núcleo de SQLAlchemy que administra el pool de conexiones con MySQL
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,  # Recicla conexiones inactivas para evitar desconexiones de MySQL
    pool_pre_ping=True  # Comprueba que la conexión esté viva antes de ejecutar una consulta
)

# 4. SessionLocal: Fábrica para crear sesiones de base de datos individuales por petición
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base: Clase padre de la cual heredarán todos nuestros modelos ORM (tablas)
Base = declarative_base()

# 6. Inyección de Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







