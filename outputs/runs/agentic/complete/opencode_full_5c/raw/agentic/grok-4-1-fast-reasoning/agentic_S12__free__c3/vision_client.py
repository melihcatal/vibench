import os
import base64
from typing import Optional


def image_to_bytes(image_path: str) -> bytes:
    """Load image bytes from local path."""
    with open(image_path, "rb") as f:
        return f.read()


def image_to_base64(image_path: str, mime_type: Optional[str] = "image/jpeg") -> str:
    """Convert image to data URL base64."""
    img_bytes = image_to_bytes(image_path)
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def get_s3_bucket() -> str:
    """Get S3 bucket from env."""
    return os.getenv("VISION_S3_BUCKET", "vision-analysis-artifacts")
