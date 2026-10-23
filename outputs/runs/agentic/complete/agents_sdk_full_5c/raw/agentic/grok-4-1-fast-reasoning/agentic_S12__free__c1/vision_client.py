import base64
from typing import Optional
from pathlib import Path

def load_image_bytes(image_path: str) -> bytes:
    """Load image file to bytes."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    with open(path, 'rb') as f:
        return f.read()

def image_to_base64(image_bytes: bytes, mime_type: str = 'image/jpeg') -> str:
    """Convert image bytes to data URL base64."""
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:{mime_type};base64,{b64}"