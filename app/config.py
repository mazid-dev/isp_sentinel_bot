# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    app_name: str = "ISP-Sentinel AI"
    debug: bool = True
    secret_key: str
    
    # Telegram
    telegram_bot_token: str
    
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # Gemini AI
    gemini_api_key: str
    
    # Redis (optional)
    redis_url: Optional[str] = "redis://localhost:6379"
    
    # MikroTik defaults
    mikrotik_api_port: int = 8728
    
    class Config:
        env_file = ".env"

settings = Settings()