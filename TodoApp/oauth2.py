from fastapi import Depends,HTTPException,status
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY= "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY= settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_token(data: dict) :
    to_encode= data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt



def verify_token(token: str, credential_exception) :
    try : 
        decoded_jwt_token= jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id : str =decoded_jwt_token.get("user_id")
        if id is None :
            raise credential_exception
        token_data = schema.TokenData(id=id)

    except JWTError :
        raise credential_exception
    
    return token_data

def fetch_logged_in_user(token: str = Depends(oauth2_scheme)) :
    credential_exception= HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token,credential_exception)