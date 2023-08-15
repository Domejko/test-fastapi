from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from . import config

from .config import settings as set

from psycopg.rows import dict_row
import time
import psycopg


SQLALCHEMY_DATABASE_URL = f'postgresql://{set.database_username}:{set.database_password}@{set.database_hostname}:{set.database_port}/{set.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=5e13bbbb", row_factory=dict_row)
#         cursor = conn.cursor()
#         print('Succesfully connected to the database.')
#         break
#     except Exception as error:
#         time.sleep(2)
#         print('Failed to connect to the database.')
#         print('Error: ', error)
