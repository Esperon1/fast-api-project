from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings
settings = Settings()


# Connection string for MySQL database
# "mysql+mysqlconnector://USER:PASSWORD@HOST:PORT/DB_NAME"
# mysqlconnector because we are using mysql-connector-python package
# SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# engine to supervise the connection pool

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Class SessionLocal will be a session factory that will create new Session objects connected to the database
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

# Base class for our models (Table)
Base = declarative_base()


# Creates a session request towards the database and closes it after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
