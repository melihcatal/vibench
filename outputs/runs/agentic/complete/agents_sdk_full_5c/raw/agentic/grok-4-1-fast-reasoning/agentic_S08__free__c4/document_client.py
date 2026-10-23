import base64
from typing import Dict, Any

def image_to_bytes(image_path: str) -> bytes:
    """Load image from file path."""
    with open(image_path, 'rb') as f:
        return f.read()

def image_bytes_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes to base64."""
    return base64.b64encode(image_bytes).decode('utf-8')