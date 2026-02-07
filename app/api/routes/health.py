"""
Health check routes.
Provides endpoints to monitor API and database health.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.database.session import get_db
from app.schemas.task import HealthResponse, DetailedHealthResponse
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Basic health check",
    description="Simple health check to verify API is running"
)
def health_check() -> HealthResponse:
    """
    Basic health check endpoint.
    
    Returns:
        Status and timestamp
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    summary="Detailed health check",
    description="Detailed health check including database connectivity"
)
def detailed_health_check(db: Session = Depends(get_db)) -> DetailedHealthResponse:
    """
    Detailed health check with database status.
    
    Checks:
    - API status
    - Database connectivity
    - API version
    
    Returns:
        Detailed health information
    """
    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        database=db_status,
        version=settings.app_version
    )
