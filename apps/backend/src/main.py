from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from core.config import config
from core.providers import AppProvider
from modules.users.provider import UsersProvider
from presentation.api.routes import setup_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = app.state.dishka_container
    
    try:
        yield
    finally:
        await container.close()


def create_app() -> FastAPI:
    app = FastAPI(title="=image_hosting_service", lifespan=lifespan)
    container = make_async_container(
        AppProvider(),
        UsersProvider(),
    )
    setup_dishka(container, app)
    app.state.dishka_container = container
    app.include_router(setup_api_router())
    return app


app = create_app()
