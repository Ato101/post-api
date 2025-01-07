from ..import schemas,models,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db
from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from typing import List
from sqlalchemy.sql import func
router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

@router.post("/", status_code= status.HTTP_201_CREATED,response_model = schemas.Post)
def create_post(new_post :schemas.PostCreate
                ,db: Session= Depends(get_db),
                current_user:int =Depends(oauth2.get_current_user) 
                ):
    print(current_user.email)
    new_data =models.Post(owner_id =current_user.id,**new_post.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

# @app.get("/posts",status_code=status.HTTP_201_CREATED)
# def create_post(ne)


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def get(id:int,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Post not found")
    return post


@router.get("/",response_model =schemas.PostResponse)
def all_post(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
#    posts= db.query(models.Post,func.count(models.Vote.post_id).label('vote')).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).order_by(models.Post.id).all()
   posts = (
    db.query(
        models.Post.id,
        models.Post.title,
        models.Post.content,
        models.Post.published,
        models.Post.owner_id,
        models.Post.owner,
        func.count(models.Vote.post_id).label("vote")
    )
    .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
    .group_by(
        models.Post.id,
        models.Post.title,
        models.Post.content,
        models.Post.published,
        models.Post.owner
    )
    .order_by(models.Post.id)
    .all()
    )
    
   return posts
@router.delete("/{id}")
def delete_post(id:int , db:Session =Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_query =db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    if current_user.id != post.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Unauthorized to perform this operatiion')
    
    post.delete(synchronize_session=False)
    db.commit()
    return status.HTTP_204_NO_CONTENTß

@router.put("/{id}",response_model = schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id== id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} is not found")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return{
        "data": post_query.first()
    }