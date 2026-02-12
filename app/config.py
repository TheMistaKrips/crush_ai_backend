from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./crush_ai.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # App
    APP_NAME: str = "CRUSH AI"
    APP_URL: str = "http://192.168.10.112:8000"
    SITE_URL: str = "http://192.168.10.112:8000"
    
    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()