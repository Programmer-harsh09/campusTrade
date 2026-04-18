"""
Category repository — read-only access to the ``categories`` table.
"""

from typing import List

from app.core.supabase_client import get_supabase_client

TABLE = "categories"


def get_all_categories() -> List[dict]:
    """Return every category, ordered by sort_order."""
    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE)
        .select("*")
        .order("sort_order", desc=False)
        .execute()
    )

    return response.data or []
