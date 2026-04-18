"""
Auth router — /signup and /login endpoints.

Uses standard Supabase email/password authentication.
"""

from fastapi import APIRouter, status

from app.schemas.auth import (
    AuthTokenResponse,
    LoginRequest,
    SignUpRequest,
    SignUpResponse,
)
from app.services.auth_service import sign_in, sign_up

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── POST /auth/signup ──────────────────────────────────────

@router.post(
    "/signup",
    response_model=SignUpResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new account",
    response_description="User created — confirmation email sent.",
)
async def signup(payload: SignUpRequest):
    """
    Create a new CampusTrade account.

    - Any valid email is accepted (no .edu restriction).
    - Password must be 8–72 characters.
    - `full_name` is optional but recommended.
    """
    result = sign_up(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
    return SignUpResponse(**result)


# ── POST /auth/login ──────────────────────────────────────

@router.post(
    "/login",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Sign in with email and password",
    response_description="JWT access and refresh tokens.",
)
async def login(payload: LoginRequest):
    """
    Authenticate and receive JWT tokens.

    Use the returned `access_token` as a Bearer token
    in the `Authorization` header for protected endpoints.
    """
    tokens = sign_in(
        email=payload.email,
        password=payload.password,
    )
    return AuthTokenResponse(**tokens)
