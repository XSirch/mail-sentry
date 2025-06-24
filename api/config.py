import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    environment: str = os.environ.get("ENVIRONMENT", "production")
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    
    # Configurações de documentação
    docs_title: str = "API de Categorização de E-mails"
    docs_description: str = "API para categorização automática de e-mails usando inteligência artificial"
    docs_version: str = "0.1.0"
    
    # Configurações de rate limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_day: int = 1000

    class Config:
        env_file = ".env"

settings = Settings()
