import os
from typing import TypeVar, Type, Any
from google.cloud import vision_v1

T = TypeVar('T')


def get_vision_client(client_class: Type[T]) -> T:
    """Initializes and returns a Google Cloud Vision client."""
    if client_class == vision_v1.ImageAnnotatorClient:
        return client_class()
    raise ValueError("Unsupported client type for Google Cloud Vision.")


def load_image_from_path(image_path: str) -> bytes:
    """Loads image data from a file path."""
    with open(image_path, "rb") as image_file:
        return image_file.read()