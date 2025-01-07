from fastapi import FastAPI,Depends,status,HTTPException
from fastapi.params import Body
from typing import Optional,List
# from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from .import models,schemas,utils
from sqlalchemy.orm import Session
from .database import engine,get_db
models.Base.metadata.create_all(bind=engine)
from .routers import post,user,auth
from fastapi.middleware.cors import CORSMiddleware

origin =["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials =True,
    allow_methods = ['*'],
    allow_headers =['*']
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

