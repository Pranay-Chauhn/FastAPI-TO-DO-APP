from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname:str
    database_password:str
    database_port:int
    database_username:str
    database_name:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int


    class Config:
        env_file = "app/.env"


settings = Settings()