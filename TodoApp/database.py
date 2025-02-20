from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

Database_URL=settings.DB_URL

engine= create_engine(Database_URL)

Sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db() :
    db=Sessionlocal() 
    try :
        yield db
    finally :
        db.close()