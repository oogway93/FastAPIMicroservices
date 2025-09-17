from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import init_db, shutdown_db
from routes import profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await shutdown_db()


app = FastAPI(
    lifespan=lifespan,
    root_path="/account",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(profile.router)
