
from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "healthy",
        "service": "oes-backend",
        "version": settings.app_version,
    }
