from pydantic import BaseModel
from typing import Union
from datetime import datetime


class CreateTask(BaseModel) :
    title : str
    description : Union[str,None]
    is_complete : bool = False

class UpdateTask(BaseModel) :
    title : Union[str,None] = None
    description : Union[str,None] = None 
    is_complete : Union[bool,None] = None

class TaskResponse(BaseModel) :
    id : int 
    title : str
    description : Union[str,None]
    is_complete : bool 
    created_at : datetime

    class config :
        orm_mode=True

class UserLogin(BaseModel) :
    pass

