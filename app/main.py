from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.items.exceptions import ItemNotFoundError
from app.items.router import router as items_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


@app.exception_handler(ItemNotFoundError)
def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.get("/", tags=["meta"])
def root():
    return {"message": f"Welcome to {settings.app_name}", "docs": "/docs"}


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


app.include_router(items_router, prefix=settings.api_prefix)
