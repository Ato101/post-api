
# After (Pydantic v2.x)
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    database_hostname :str
    database_password:str
    database_name: str
    database_port:str
    database_username: str
    algorithm:str
    secret_key: str
    access_token_expire_time:int


    class Config:
        env_file = ".env"

settings = Settings()
