from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"


class Settings(BaseSettings):
    token: str
    support_chat_id: str
    feedback_chat_id: str

    class Config:
        env_file = BASE_DIR / ".env"


config = Settings()

TOKEN = config.token
SUPPORT_CHAT_ID = config.support_chat_id
FEEDBACK_CHAT_ID = config.feedback_chat_id
