import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"
    
    # Adicione outras configurações específicas aqui
    # Por exemplo, URLs de serviços externos, etc.
    
    class Config:
        env_file = ".env"

settings = Settings()