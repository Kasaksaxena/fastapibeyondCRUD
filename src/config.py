from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    database_url:str
    # Load from .env file located one directory level up
    model_config=SettingsConfigDict(env_file=os.path.join('..','.env'))
    


settings=Settings()