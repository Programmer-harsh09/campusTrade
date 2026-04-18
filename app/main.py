"""
CampusTrade API — Application Entry Point

A student marketplace backend built with FastAPI and Supabase.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.health import router as health_router
from app.core.config import get_settings

# ── Initialise settings ─────────────────────────────────────────
settings = get_settings()

# ── Create FastAPI application ──────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "CampusTrade is a peer-to-peer marketplace for college students "
        "to buy, sell, and trade textbooks, electronics, and more."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ─────────────────────────────────────────────
# In production, replace the wildcard with your actual frontend origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # TODO: lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ───────────────────────────────────────────
app.include_router(health_router)

# ── Root Endpoint ──────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    """Redirect-friendly landing that confirms the API is running."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "health": "/health",
    }
