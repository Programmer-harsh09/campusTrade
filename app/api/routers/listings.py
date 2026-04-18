"""
Listings router — RESTful CRUD endpoints for marketplace listings.

Public:   GET /listings, GET /listings/{id}
Private:  POST /listings, PUT /listings/{id}, DELETE /listings/{id}
          GET /listings/me  (authenticated user's own listings)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.core.auth_dependency import get_current_user_id
from app.repositories import listing_repo
from app.schemas.listing import (
    ListingCreate,
    ListingResponse,
    ListingUpdate,
)

router = APIRouter(prefix="/listings", tags=["Listings"])


# ── POST /listings ─────────────────────────────────────────
@router.post(
    "",
    response_model=ListingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new listing",
    response_description="The newly created listing.",
)
async def create_listing(
    payload: ListingCreate,
    user_id: str = Depends(get_current_user_id),
):
    """
    Create a marketplace listing for the authenticated user.

    Requires a valid Bearer token in the ``Authorization`` header.
    """
    data = payload.model_dump(mode="json")
    row = listing_repo.create_listing(user_id, data)
    return row


# ── GET /listings ──────────────────────────────────────────
@router.get(
    "",
    response_model=List[ListingResponse],
    summary="Browse listings",
    response_description="Paginated list of listings.",
)
async def list_listings(
    status_filter: Optional[str] = Query(
        "active",
        alias="status",
        description="Filter by listing status (active, sold, archived, draft). "
                    "Pass empty string for all.",
    ),
    category_id: Optional[str] = Query(
        None,
        description="Filter by category UUID.",
    ),
    search: Optional[str] = Query(
        None,
        description="Full-text search on title.",
    ),
    limit: int = Query(20, ge=1, le=100, description="Page size."),
    offset: int = Query(0, ge=0, description="Number of rows to skip."),
):
    """
    Browse marketplace listings with optional filters and pagination.

    Open to everyone — no authentication required.
    """
    # Treat empty string as "no filter"
    effective_status = status_filter if status_filter else None

    rows = listing_repo.get_listings(
        status_filter=effective_status,
        category_id=category_id,
        search=search,
        limit=limit,
        offset=offset,
    )
    return rows


# ── GET /listings/me ───────────────────────────────────────
@router.get(
    "/me",
    response_model=List[ListingResponse],
    summary="My listings",
    response_description="All listings belonging to the authenticated user.",
)
async def my_listings(
    user_id: str = Depends(get_current_user_id),
):
    """Return every listing owned by the currently authenticated seller."""
    rows = listing_repo.get_my_listings(user_id)
    return rows


# ── GET /listings/{listing_id} ─────────────────────────────
@router.get(
    "/{listing_id}",
    response_model=ListingResponse,
    summary="Get a listing by ID",
    response_description="Full listing object.",
)
async def get_listing(listing_id: str):
    """Fetch a single listing by its UUID. Public endpoint."""
    row = listing_repo.get_listing_by_id(listing_id)
    return row


# ── PUT /listings/{listing_id} ─────────────────────────────
@router.put(
    "/{listing_id}",
    response_model=ListingResponse,
    summary="Update a listing",
    response_description="The updated listing.",
)
async def update_listing(
    listing_id: str,
    payload: ListingUpdate,
    user_id: str = Depends(get_current_user_id),
):
    """
    Update an existing listing.

    Only the seller who created the listing can modify it.
    Only fields present in the request body are updated.
    """
    updates = payload.model_dump(exclude_unset=True, mode="json")
    if not updates:
        # Nothing to update — return existing row
        return listing_repo.get_listing_by_id(listing_id)

    row = listing_repo.update_listing(listing_id, user_id, updates)
    return row


# ── DELETE /listings/{listing_id} ──────────────────────────
@router.delete(
    "/{listing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a listing",
)
async def delete_listing(
    listing_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """
    Permanently delete a listing.

    Only the seller who created the listing can delete it.
    """
    listing_repo.delete_listing(listing_id, user_id)
