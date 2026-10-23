import os
import base64


def load_image_bytes(image_path: str) -> bytes:
    """Load image file to bytes."""
    with open(image_path, "rb") as f:
        return f.read()


def b64_image(image_path: str) -> str:
    """Encode image to base64 string."""
    return base64.b64encode(load_image_bytes(image_path)).decode("utf-8")
