from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int 

    #loading .env
    class Config:
        env_file = ".env"

settings = Settings()
