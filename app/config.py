import os 
from dotenv import load_dotenv

load_dotenv

class Settings:
    GATEWAY_SECRET_KEY: str = os.getenv("GATEWAY_SECRET_KEY", "default_secret_key")
    TARGET_BACKEND_URL: str = os.getenv("TARGET_BACKEND_URL", "http://localhost:8001")
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

settings = Settings()