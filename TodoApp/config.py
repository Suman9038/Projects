from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings) :
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    # OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config :
        env_nested_delimiter = "__"


settings = Settings(_env_file= os.path.join(os.getcwd(), "TodoApp/.env"))