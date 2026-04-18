"""
Auth dependency — verifies the Supabase JWT and returns the current user ID.

Usage in any route:
    from app.core.auth_dependency import get_current_user_id

    @router.post("/something")
    async def do_something(user_id: str = Depends(get_current_user_id)):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.supabase_client import get_supabase_client

# Scheme used in OpenAPI docs — adds a padlock icon + "Authorize" button
_bearer_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> str:
    """
    Validate the Bearer token via Supabase ``auth.get_user()``.

    Returns:
        The authenticated user's UUID as a string.

    Raises:
        HTTPException 401 if the token is missing, expired, or invalid.
    """
    token = credentials.credentials
    supabase = get_supabase_client()

    try:
        response = supabase.auth.get_user(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if response is None or response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return str(response.user.id)
