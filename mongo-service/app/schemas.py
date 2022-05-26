from pydantic import BaseModel


class Info(BaseModel):
    """Basic model to keep all the information about the app
    """
    running: bool
    name: str
    version: str

    class Config:
        schema_extra = {"example": {"running": True, "appName": "An app name taken from the settings", "appVersion": "An app version taken from the settings"}}