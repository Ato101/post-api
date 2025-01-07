from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from .import schemas,models
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

# This function is to help us to set a constriant on some certain path eg login is required before you used some certain path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


## Generating Access token for verification
def create_access_token(data:dict):

    encode_data = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)

    encode_data.update({'exp':expire})

    encode_jwt=jwt.encode(encode_data,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

# verifying the the access token if it is valid or not valid 
def verify_access_token(token:str,credentials_exception):

    try:
        payload =jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    return token_data
# Getting the current user through using the token 
def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid crendentials"
                                         ,headers={'WWW-Authenticate':'Bearer'})
    token = verify_access_token(
        token,credentials_exception
    )
    user = db.query(models.Users).filter(models.Users.id==token.id).first()
    
    return user