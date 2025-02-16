from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

class User(Base) : 
    __tablename__="users"

    id=Column(Integer,primary_key=True,nullable=False)
    username=Column(String(255),unique=True,index=True,nullable=False)
    password=Column(String(255),nullable=False)
    created_at=(Column(TIMESTAMP,nullable=False,server_default=text('now()')))


class Task(Base) :
    __tablename__ ="tasks"

    id=Column(Integer,primary_key=True,nullable=False,index=True)
    title=Column(String(255),nullable=False,index=True)
    description=Column(String(255),nullable=False,default="")
    created_at=(Column(TIMESTAMP,nullable=False,server_default=text('now()')))
    is_complete=Column(Boolean,default=False)
    priority= Column(String(255),nullable=False,default="MEDIUM")
    user_id= Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
