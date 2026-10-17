
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, memories
from app.core.config import settings
from app.core.database import initialize_database
from app.core.logging_config import configure_logging
from app.models.schemas import RootResponse

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.app_name)
    initialize_database()
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="A local-first AI system for remembering your learning journey.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(memories.router, prefix=settings.api_prefix)


@app.get("/", response_model=RootResponse)
def root():
    logger.debug("Root endpoint requested")

    return {
        "message": "Welcome to OES",
        "status": "running",
    }
