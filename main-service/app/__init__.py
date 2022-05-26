from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app(*args, **kwargs) -> FastAPI:
    """Basic factory method to create and inint properly
    the FastApi instance.
    Use that factory method for development and production ready purposes.

    Returns:
        FastAPI: Prepared FastAPI instance.
    """
    from app.settings import settings
    from app.routers import router

    # Instanciate app
    app = FastAPI(title=settings.app_name, version=settings.app_version, debug=True)

    # Add CORS support
    app.add_middleware(
        CORSMiddleware, allow_origins=("*",), allow_methods=("*",), allow_headers=("*",)
    )

    # Add router
    app.include_router(router)

    return app
