from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base,Relationship
Base = declarative_base()


class Users(Base):
    __tablename__ = "tblUsers"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
class Post(Base):
    __tablename__= 'posts'
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(String,default=True)
    owner_id = Column(Integer,ForeignKey('tblUsers.id',ondelete='CASCADE'),nullable=False)
    owner = Relationship("Users")

class Vote(Base):
    __tablename__ = 'tblVote'
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),nullable=False)
    user_id = Column(Integer,ForeignKey('tblUsers.id',ondelete='CASCADE'),nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('post_id', 'user_id'),  # Composite primary key
    )