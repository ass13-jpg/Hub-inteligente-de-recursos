from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Banco de dados
    DATABASE_URL: str = "sqlite:///./educational_hub.db"
    
    # IA
    GEMINI_API_KEY: str
    AI_MODEL: str = "gemini-1.5-flash"
    
    # API
    API_TITLE: str = "Educational Hub API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
