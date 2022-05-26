from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    """Class describing general settings. All
    Settings must be here."""

    app_name: str = Field(..., env="MONGO_SERVICE_APP_NAME")
    app_version: str = Field(..., env="MONGO_SERVICE_APP_VERSION")


settings = Settings()