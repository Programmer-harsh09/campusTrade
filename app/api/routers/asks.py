"""
Asks router — RESTful CRUD endpoints for buy-requests ("Ask Mode").

Public:   GET /asks, GET /asks/{id}
Private:  POST /asks, PUT /asks/{id}, DELETE /asks/{id}
          GET /asks/me  (authenticated user's own asks)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.core.auth_dependency import get_current_user_id
from app.repositories import ask_repo
from app.schemas.ask import (
    AskCreate,
    AskResponse,
    AskUpdate,
)

router = APIRouter(prefix="/asks", tags=["Asks (Buy Requests)"])


# ── POST /asks ─────────────────────────────────────────────
@router.post(
    "",
    response_model=AskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new buy-request",
    response_description="The newly created ask.",
)
async def create_ask(
    payload: AskCreate,
    user_id: str = Depends(get_current_user_id),
):
    """
    Post a new buy-request (ask) for the authenticated user.

    Requires a valid Bearer token in the ``Authorization`` header.
    """
    data = payload.model_dump(mode="json")
    row = ask_repo.create_ask(user_id, data)
    return row


# ── GET /asks ──────────────────────────────────────────────
@router.get(
    "",
    response_model=List[AskResponse],
    summary="Browse buy-requests",
    response_description="Paginated list of asks.",
)
async def list_asks(
    status_filter: Optional[str] = Query(
        "open",
        alias="status",
        description="Filter by ask status (open, fulfilled, closed). "
                    "Pass empty string for all.",
    ),
    category_id: Optional[str] = Query(
        None,
        description="Filter by category UUID.",
    ),
    urgency: Optional[str] = Query(
        None,
        description="Filter by urgency (low, medium, high).",
    ),
    search: Optional[str] = Query(
        None,
        description="Full-text search on title.",
    ),
    limit: int = Query(20, ge=1, le=100, description="Page size."),
    offset: int = Query(0, ge=0, description="Number of rows to skip."),
):
    """
    Browse buy-requests with optional filters and pagination.

    Open to everyone — no authentication required.
    """
    effective_status = status_filter if status_filter else None

    rows = ask_repo.get_asks(
        status_filter=effective_status,
        category_id=category_id,
        urgency=urgency,
        search=search,
        limit=limit,
        offset=offset,
    )
    return rows


# ── GET /asks/me ───────────────────────────────────────────
@router.get(
    "/me",
    response_model=List[AskResponse],
    summary="My buy-requests",
    response_description="All asks belonging to the authenticated user.",
)
async def my_asks(
    user_id: str = Depends(get_current_user_id),
):
    """Return every ask owned by the currently authenticated user."""
    rows = ask_repo.get_my_asks(user_id)
    return rows


# ── GET /asks/{ask_id} ─────────────────────────────────────
@router.get(
    "/{ask_id}",
    response_model=AskResponse,
    summary="Get a buy-request by ID",
    response_description="Full ask object.",
)
async def get_ask(ask_id: str):
    """Fetch a single ask by its UUID. Public endpoint."""
    row = ask_repo.get_ask_by_id(ask_id)
    return row


# ── PUT /asks/{ask_id} ─────────────────────────────────────
@router.put(
    "/{ask_id}",
    response_model=AskResponse,
    summary="Update a buy-request",
    response_description="The updated ask.",
)
async def update_ask(
    ask_id: str,
    payload: AskUpdate,
    user_id: str = Depends(get_current_user_id),
):
    """
    Update an existing ask.

    Only the requester who created the ask can modify it.
    Only fields present in the request body are updated.
    """
    updates = payload.model_dump(exclude_unset=True, mode="json")
    if not updates:
        return ask_repo.get_ask_by_id(ask_id)

    row = ask_repo.update_ask(ask_id, user_id, updates)
    return row


# ── DELETE /asks/{ask_id} ──────────────────────────────────
@router.delete(
    "/{ask_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a buy-request",
)
async def delete_ask(
    ask_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """
    Permanently delete an ask.

    Only the requester who created the ask can delete it.
    """
    ask_repo.delete_ask(ask_id, user_id)
