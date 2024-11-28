from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Database_URL="mysql://root:suman2003@localhost/todo"

engine= create_engine(Database_URL)

Sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db() :
    db=Sessionlocal() 
    try :
        yield db
    finally :
        db.close()