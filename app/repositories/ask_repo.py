"""
Ask repository — Supabase CRUD operations for the ``asks`` table.
"""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status

from app.core.supabase_client import get_supabase_client

TABLE = "asks"


# ── Helpers ────────────────────────────────────────────────

def _row_or_404(data: list, ask_id: str) -> dict:
    """Return the single row or raise 404."""
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ask {ask_id} not found.",
        )
    return data[0]


def _assert_owner(row: dict, user_id: str) -> None:
    """Ensure the authenticated user owns the ask."""
    if row.get("requester_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this ask.",
        )


# ── CREATE ─────────────────────────────────────────────────

def create_ask(user_id: str, payload: Dict[str, Any]) -> dict:
    """
    Insert a new ask / buy-request for the authenticated user.

    ``payload`` should be a dict built from ``AskCreate.model_dump()``.
    """
    supabase = get_supabase_client()
    payload["requester_id"] = user_id

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
            detail="Failed to create ask.",
        )

    return response.data[0]


# ── READ (single) ─────────────────────────────────────────

def get_ask_by_id(ask_id: str) -> dict:
    """Fetch a single ask by primary key."""
    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("id", ask_id)
        .execute()
    )

    return _row_or_404(response.data, ask_id)


# ── READ (list) ────────────────────────────────────────────

def get_asks(
    *,
    status_filter: Optional[str] = "open",
    category_id: Optional[str] = None,
    urgency: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[dict]:
    """
    Return a paginated list of asks.

    Supports optional filters: status, category, urgency, and full-text search.
    """
    supabase = get_supabase_client()

    query = supabase.table(TABLE).select("*")

    if status_filter:
        query = query.eq("status", status_filter)

    if category_id:
        query = query.eq("category_id", category_id)

    if urgency:
        query = query.eq("urgency", urgency)

    if search:
        query = query.text_search(
            "title",
            search,
            options={"type": "websearch"},
        )

    query = query.order("created_at", desc=True)
    query = query.range(offset, offset + limit - 1)

    response = query.execute()
    return response.data or []


# ── READ (my asks) ─────────────────────────────────────────

def get_my_asks(user_id: str) -> List[dict]:
    """Return all asks owned by the authenticated user."""
    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("requester_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


# ── UPDATE ─────────────────────────────────────────────────

def update_ask(
    ask_id: str,
    user_id: str,
    updates: Dict[str, Any],
) -> dict:
    """
    Update an ask only if the authenticated user is the requester.

    ``updates`` should be a dict built from
    ``AskUpdate.model_dump(exclude_unset=True)``.
    """
    existing = get_ask_by_id(ask_id)
    _assert_owner(existing, user_id)

    # Convert UUID values to strings
    if "category_id" in updates and updates["category_id"] is not None:
        updates["category_id"] = str(updates["category_id"])

    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .update(updates)
        .eq("id", ask_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update ask.",
        )

    return response.data[0]


# ── DELETE ─────────────────────────────────────────────────

def delete_ask(ask_id: str, user_id: str) -> None:
    """
    Hard-delete an ask only if the authenticated user is the requester.
    """
    existing = get_ask_by_id(ask_id)
    _assert_owner(existing, user_id)

    supabase = get_supabase_client()

    supabase.table(TABLE).delete().eq("id", ask_id).execute()
