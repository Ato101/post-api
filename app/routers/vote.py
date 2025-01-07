from fastapi import HTTPException,status,APIRouter,Depends
from ..import schemas,oauth2,models
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags='Vote'
)


router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   #Checking to see if entry already exits in our vote table
   vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                             models.Vote.user_id == current_user.id)
   found_vote = vote_query.first()
   if (vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='User alredy voted')
        new_entry= models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_entry)
        db.commit()
        return{"message":"created Sucessfully"}
   else:
       if not found_vote:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Entry not Found')
       vote_query.delete(synchronize_session=False)
       db.commit()
        

      
    
  
        