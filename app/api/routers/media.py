"""
Media router — image upload endpoint.

Authenticated users can upload images; the public URL is returned.
"""

from fastapi import APIRouter, Depends, UploadFile, File, status

from app.core.auth_dependency import get_current_user_id
from app.services.media_service import upload_image

router = APIRouter(prefix="/media", tags=["Media"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload an image",
    response_description="Public URL of the uploaded image.",
)
async def upload_media(
    file: UploadFile = File(
        ...,
        description="Image file to upload (JPEG, PNG, or WebP, max 5 MB).",
    ),
    user_id: str = Depends(get_current_user_id),
):
    """
    Upload an image to CampusTrade media storage.

    Requires a valid Bearer token. The file must be JPEG, PNG, or WebP
    and must not exceed 5 MB.

    Returns the public URL of the stored image.
    """
    public_url = await upload_image(file)

    return {
        "message": "Image uploaded successfully.",
        "url": public_url,
    }
