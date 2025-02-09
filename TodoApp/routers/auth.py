from fastapi import FastAPI,APIRouter,HTTPException,Response,status,Depends
from sqlalchemy.orm import Session
from ..import schema,database,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=["User Registrarion and Login"])

@router.post("/register",response_model=schema.UserResponse)
def user_registration(user : OAuth2PasswordRequestForm =Depends(),db :Session=Depends(database.get_db)) :
    hashed_password=utils.hash(user.password)
    # user.password=hashed_password
    existing_user=db.query(models.User).filter(models.User.username==user.username).first()
    if existing_user :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Username is already exists try with new username")
    new_user=models.User(username=user.username , password= hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model= schema.TokenResponse)
def user_login(user_credentials: OAuth2PasswordRequestForm =Depends(),db : Session = Depends(database.get_db)) :
    user = db.query(models.User).filter(models.User.username==user_credentials.username).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Not Found With this Username")
    if not utils.verify(user_credentials.password , user.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Not Found With this Password ")
    
    access_token=oauth2.create_token(data={"user_id" : user.id})
    return{"access_token" : access_token , "token_type" : "bearer"}