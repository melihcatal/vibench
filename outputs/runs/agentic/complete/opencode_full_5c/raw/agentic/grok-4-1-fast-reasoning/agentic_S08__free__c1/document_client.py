import os
import base64
from typing import Union


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        return image_file.read()


def load_image_base64(image_path: str) -> str:
    image_bytes = load_image_bytes(image_path)
    return base64.b64encode(image_bytes).decode("utf-8")


def get_mime_type(image_path: str) -> str:
    lower_path = image_path.lower()
    if lower_path.endswith(".pdf"):
        return "application/pdf"
    elif lower_path.endswith(".png"):
        return "image/png"
    elif lower_path.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    raise ValueError(f"Unsupported image type for {image_path}")
