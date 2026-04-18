"""
Media service — handles image validation and upload to Supabase Storage.

Supported formats: JPEG, PNG, WebP.
Max file size: 5 MB.
"""

import uuid
from pathlib import PurePosixPath

from fastapi import HTTPException, UploadFile, status

from app.core.supabase_client import get_supabase_client

# ── Constants ──────────────────────────────────────────────
BUCKET_NAME = "media"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_CONTENT_TYPES: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


# ── Public API ─────────────────────────────────────────────

async def upload_image(file: UploadFile) -> str:
    """
    Validate and upload an image to Supabase Storage.

    Args:
        file: A FastAPI ``UploadFile`` coming from a multipart form.

    Returns:
        The public URL of the uploaded image.

    Raises:
        HTTPException 400 if the file type is unsupported or exceeds 5 MB.
        HTTPException 500 if the Supabase upload fails.
    """

    # 1. Validate MIME type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type '{content_type}'. "
                f"Allowed: {', '.join(ALLOWED_CONTENT_TYPES.keys())}."
            ),
        )

    # 2. Read file bytes and validate size
    file_bytes = await file.read()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"File too large ({len(file_bytes) / (1024 * 1024):.1f} MB). "
                f"Maximum allowed size is {MAX_FILE_SIZE / (1024 * 1024):.0f} MB."
            ),
        )

    # 3. Build a unique storage path  (e.g.  "uploads/a1b2c3d4.jpg")
    extension = ALLOWED_CONTENT_TYPES[content_type]
    unique_name = f"{uuid.uuid4().hex}{extension}"
    storage_path = str(PurePosixPath("uploads", unique_name))

    # 4. Upload to Supabase Storage
    supabase = get_supabase_client()

    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload to Supabase Storage failed: {exc}",
        )

    # 5. Retrieve and return the public URL
    public_url = (
        supabase.storage.from_(BUCKET_NAME)
        .get_public_url(storage_path)
    )

    return public_url
