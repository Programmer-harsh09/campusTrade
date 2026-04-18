"""
Health-check router.

Provides liveness and readiness probes for monitoring
and container orchestration.
"""

from fastapi import APIRouter, status

from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
    response_description="Service is alive",
)
async def health_check():
    """Return basic service health information."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
