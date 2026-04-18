"""
Listing schemas — request and response models for marketplace listings.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Enums (mirror the PostgreSQL enums) ────────────────────

class ListingStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    ARCHIVED = "archived"


class ListingCondition(str, Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


# ── Create Model ───────────────────────────────────────────

class ListingCreate(BaseModel):
    """Payload for creating a new listing."""

    category_id: UUID = Field(
        ...,
        description="FK to categories table.",
    )
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Listing title (3–200 chars).",
    )
    description: str = Field(
        "",
        max_length=5000,
        description="Detailed description (max 5000 chars).",
    )
    price: float = Field(
        ...,
        gt=0,
        description="Asking price — must be greater than 0.",
    )
    condition: ListingCondition = Field(
        ListingCondition.GOOD,
        description="Item condition.",
    )
    images: List[str] = Field(
        default_factory=list,
        max_length=10,
        description="Up to 10 Supabase Storage URLs.",
    )


# ── Update Model ───────────────────────────────────────────

class ListingUpdate(BaseModel):
    """Fields a seller can update on their listing."""

    category_id: Optional[UUID] = None
    title: Optional[str] = Field(
        None, min_length=3, max_length=200,
    )
    description: Optional[str] = Field(
        None, max_length=5000,
    )
    price: Optional[float] = Field(
        None, gt=0,
    )
    condition: Optional[ListingCondition] = None
    status: Optional[ListingStatus] = None
    images: Optional[List[str]] = Field(
        None, max_length=10,
    )


# ── Response Model ─────────────────────────────────────────

class ListingResponse(BaseModel):
    """Full listing data returned by the API."""

    id: UUID
    seller_id: UUID
    category_id: UUID
    title: str
    description: str
    price: float
    condition: ListingCondition
    status: ListingStatus
    images: List[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
