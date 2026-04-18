"""
Auth schemas — request models for signup / login and token responses.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ── Request Models ─────────────────────────────────────────

class SignUpRequest(BaseModel):
    """Payload for new user registration."""

    email: EmailStr = Field(
        ...,
        description="Any valid email address.",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password (8–72 chars).",
    )
    full_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Display name stored in user metadata.",
    )


class LoginRequest(BaseModel):
    """Payload for email/password sign-in."""

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
    )
    password: str = Field(
        ...,
        min_length=1,
        description="Account password.",
    )


# ── Response Models ────────────────────────────────────────

class AuthTokenResponse(BaseModel):
    """Tokens returned after successful login."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(
        ...,
        description="Token lifetime in seconds.",
    )


class SignUpResponse(BaseModel):
    """Response after successful registration."""

    message: str = "Registration successful. Please check your email to confirm your account."
    user_id: str
    email: str
