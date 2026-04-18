"""
Authentication service — wrappers around Supabase GoTrue auth.

Handles standard email/password sign-up and sign-in.
No .edu domain restriction — any valid email is accepted.
"""

from fastapi import HTTPException, status
from gotrue.errors import AuthApiError

from app.core.supabase_client import get_supabase_client


# ── Sign Up ────────────────────────────────────────────────

def sign_up(email: str, password: str, full_name: str | None = None) -> dict:
    """
    Register a new user with Supabase Auth.

    The handle_new_user() DB trigger automatically creates
    a matching profiles row on success.

    Returns:
        dict with user id, email, and confirmation message.

    Raises:
        HTTPException 400 on validation / duplicate-email errors.
    """
    supabase = get_supabase_client()

    # Build metadata dict (passed to raw_user_meta_data in auth.users)
    metadata = {}
    if full_name:
        metadata["full_name"] = full_name

    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": metadata} if metadata else {},
            }
        )
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    user = response.user
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sign-up failed. The email may already be registered.",
        )

    return {
        "user_id": str(user.id),
        "email": user.email,
    }


# ── Sign In ────────────────────────────────────────────────

def sign_in(email: str, password: str) -> dict:
    """
    Authenticate an existing user with email + password.

    Returns:
        dict with access_token, refresh_token, token_type,
        and expires_in.

    Raises:
        HTTPException 401 on invalid credentials.
    """
    supabase = get_supabase_client()

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )

    session = response.session
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "token_type": "bearer",
        "expires_in": session.expires_in,
    }
