from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#engine is responsible for making the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This is the function to connect db and get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# while True:
        
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi2',
#                                 user='postgres', password='E2b76b8d', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(3)