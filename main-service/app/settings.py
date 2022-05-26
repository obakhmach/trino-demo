from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    """Class describing general settings. All
    Settings must be here."""

    app_name: str = Field(..., env="MAIN_SERVICE_APP_NAME")
    app_version: str = Field(..., env="MAIN_SERVICE_APP_VERSION")
    trino_coordinator_host: str = Field(..., env="TRINO_COORDINATOR_HOST")
    trino_coordinator_port: str = Field(..., env="TRINO_COORDINATOR_PORT")
    redis_password: str = Field(..., env="REDIS_PASSWORD")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: str = Field(..., env="REDIS_PORT")

    @property
    def trino_coordinator_url(self) -> str:
        """Getter to return the trino coordinator url"""
        return f"http://{self.trino_coordinator_host}:{self.trino_coordinator_port}"


settings = Settings()
