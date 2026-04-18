"""
Profile schemas — request and response models for user profiles.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Response Models ─────────────────────────────────────────

class ProfileResponse(BaseModel):
    """Public profile data returned by the API."""

    id: UUID
    full_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = ""
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Update Models ───────────────────────────────────────────

class ProfileUpdate(BaseModel):
    """Fields a user can update on their own profile."""

    full_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Display name (1–100 chars).",
    )
    avatar_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to avatar image in Supabase Storage.",
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="Short bio (max 500 chars).",
    )
