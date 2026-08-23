import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    YOUCONTROL_API_KEY: str = ""
    GETCONTACT_TOKEN: str = ""
    PROXY_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
