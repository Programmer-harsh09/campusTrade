"""
Categories router — public read-only endpoint for product categories.
"""

from typing import List

from fastapi import APIRouter

from app.repositories import category_repo

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    summary="List all categories",
    response_description="All available product categories.",
)
async def list_categories():
    """
    Return every category ordered by sort_order.

    Public endpoint — no authentication required.
    """
    return category_repo.get_all_categories()
