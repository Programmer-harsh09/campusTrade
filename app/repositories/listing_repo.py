"""
Listing repository — Supabase CRUD operations for the ``listings`` table.
"""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status

from app.core.supabase_client import get_supabase_client

TABLE = "listings"


# ── Helpers ────────────────────────────────────────────────

def _row_or_404(data: list, listing_id: str) -> dict:
    """Return the single row or raise 404."""
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Listing {listing_id} not found.",
        )
    return data[0]


def _assert_owner(row: dict, user_id: str) -> None:
    """Ensure the authenticated user owns the listing."""
    if row.get("seller_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this listing.",
        )


# ── CREATE ─────────────────────────────────────────────────

def create_listing(user_id: str, payload: Dict[str, Any]) -> dict:
    """
    Insert a new listing for the authenticated seller.

    ``payload`` should be a dict built from ``ListingCreate.model_dump()``.
    """
    supabase = get_supabase_client()
    payload["seller_id"] = user_id

    # Convert UUID values to strings for JSON serialisation
    if "category_id" in payload and payload["category_id"] is not None:
        payload["category_id"] = str(payload["category_id"])

    response = (
        supabase.table(TABLE)
        .insert(payload)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create listing.",
        )

    return response.data[0]


# ── READ (single) ─────────────────────────────────────────

def get_listing_by_id(listing_id: str) -> dict:
    """Fetch a single listing by primary key."""
    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("id", listing_id)
        .execute()
    )

    return _row_or_404(response.data, listing_id)


# ── READ (list) ────────────────────────────────────────────

def get_listings(
    *,
    status_filter: Optional[str] = "active",
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[dict]:
    """
    Return a paginated list of listings.

    Supports optional filters: status, category, and full-text search.
    """
    supabase = get_supabase_client()

    query = supabase.table(TABLE).select("*")

    if status_filter:
        query = query.eq("status", status_filter)

    if category_id:
        query = query.eq("category_id", category_id)

    if search:
        # Use Supabase full-text search on title + description
        query = query.text_search(
            "title",
            search,
            options={"type": "websearch"},
        )

    query = query.order("created_at", desc=True)
    query = query.range(offset, offset + limit - 1)

    response = query.execute()
    return response.data or []


# ── READ (my listings) ─────────────────────────────────────

def get_my_listings(user_id: str) -> List[dict]:
    """Return all listings owned by the authenticated user."""
    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("seller_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


# ── UPDATE ─────────────────────────────────────────────────

def update_listing(
    listing_id: str,
    user_id: str,
    updates: Dict[str, Any],
) -> dict:
    """
    Update a listing only if the authenticated user is the seller.

    ``updates`` should be a dict built from
    ``ListingUpdate.model_dump(exclude_unset=True)``.
    """
    # Ownership check
    existing = get_listing_by_id(listing_id)
    _assert_owner(existing, user_id)

    # Convert UUID values to strings
    if "category_id" in updates and updates["category_id"] is not None:
        updates["category_id"] = str(updates["category_id"])

    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .update(updates)
        .eq("id", listing_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update listing.",
        )

    return response.data[0]


# ── DELETE ─────────────────────────────────────────────────

def delete_listing(listing_id: str, user_id: str) -> None:
    """
    Hard-delete a listing only if the authenticated user is the seller.
    """
    existing = get_listing_by_id(listing_id)
    _assert_owner(existing, user_id)

    supabase = get_supabase_client()

    supabase.table(TABLE).delete().eq("id", listing_id).execute()
