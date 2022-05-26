from fastapi import APIRouter

from app.schemas import Info as InfoSchema
from app.settings import settings


router = APIRouter()


@router.get(
    "/",
    response_model=InfoSchema,
    tags=["index"],
)
async def index() -> InfoSchema:
    """Return the list of the all available videos to view."""
    return InfoSchema(running=True,  name=settings.app_name, version=settings.app_version)