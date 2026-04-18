"""
Ask schemas — request and response models for buy-requests.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Enums (mirror the PostgreSQL enums) ────────────────────

class AskStatus(str, Enum):
    OPEN = "open"
    FULFILLED = "fulfilled"
    CLOSED = "closed"


class AskUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ── Create Model ───────────────────────────────────────────

class AskCreate(BaseModel):
    """Payload for creating a new ask / buy-request."""

    category_id: UUID = Field(
        ...,
        description="FK to categories table.",
    )
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="What are you looking for? (3–200 chars).",
    )
    description: str = Field(
        "",
        max_length=3000,
        description="Extra details about the request (max 3000 chars).",
    )
    budget_max: Optional[float] = Field(
        None,
        ge=0,
        description="Maximum budget — null means no limit.",
    )
    urgency: AskUrgency = Field(
        AskUrgency.MEDIUM,
        description="How urgently you need this.",
    )


# ── Update Model ───────────────────────────────────────────

class AskUpdate(BaseModel):
    """Fields a requester can update on their ask."""

    category_id: Optional[UUID] = None
    title: Optional[str] = Field(
        None, min_length=3, max_length=200,
    )
    description: Optional[str] = Field(
        None, max_length=3000,
    )
    budget_max: Optional[float] = Field(
        None, ge=0,
    )
    urgency: Optional[AskUrgency] = None
    status: Optional[AskStatus] = None


# ── Response Model ─────────────────────────────────────────

class AskResponse(BaseModel):
    """Full ask data returned by the API."""

    id: UUID
    requester_id: UUID
    category_id: UUID
    title: str
    description: str
    budget_max: Optional[float]
    urgency: AskUrgency
    status: AskStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
