import base64
import os
from typing import Union

def image_to_bytes(image_path: str) -> bytes:
    """Load image file to bytes."""
    with open(image_path, 'rb') as f:
        return f.read()

def image_to_base64(image_path: str) -> str:
    """Load image file to base64 encoded string."""
    return base64.b64encode(image_to_bytes(image_path)).decode('utf-8')