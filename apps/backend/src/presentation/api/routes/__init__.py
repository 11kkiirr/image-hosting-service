from fastapi import APIRouter


def setup_api_router() -> APIRouter:
    router = APIRouter()
    
    # from .webhook import telegram
    
    # router.include_router(telegram.router)
    
    return router
