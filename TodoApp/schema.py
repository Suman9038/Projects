from pydantic import BaseModel,EmailStr
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
    priority: str
    user_id: int
    created_at : datetime

    class config :
        orm_mode=True

class CreateUser(BaseModel) :
    username : EmailStr
    password :str

class UserResponse(BaseModel) :
    username : str
    id : int
    created_at : datetime

class UserLogin(BaseModel) :
    username : EmailStr
    password : str

class TokenResponse(BaseModel) :
    access_token : str
    token_type: str

class TokenData(BaseModel) :
    id: Union[int,None]=None