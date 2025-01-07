from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..import models,schemas,utils,oauth2
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
router = APIRouter(
    tags= ['Login']
)



@router.post("/login")
def Login(user_credentials:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email== 
                                         user_credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credential")
    
    if not utils.verify_pwd(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    #generate token

    token= oauth2.create_access_token(data={"user_id":user.id})
    print(token)
    return {"access_token": token,"token_type":"bearer"}