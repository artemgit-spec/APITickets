from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALGORITHM: str = 'HS256'
    SECRET_KEY: str = "aaf3242fdbcv"
    EXPIRES_TIME_TOXEN: int = 30
    
    
settings = Settings()