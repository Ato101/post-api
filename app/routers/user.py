from ..import schemas,utils,models
from ..database import get_db
from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=['user']
)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model =schemas.UserResponse) 
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password =utils.hash_pwd(user.password)
        user.password = hashed_password
        new_user = models.Users(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user.email}' already exists."
        )
    except ValueError as e:
        db.rollback()  # Rollback the transaction for any other exceptions
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_user


@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND
                            ,detail=f"user with id: {id} not found")
    
    return user