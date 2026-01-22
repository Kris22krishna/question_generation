from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Backend Configuration
    BACKEND_CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"
    
    # Execution Configuration
    EXECUTION_TIMEOUT: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
