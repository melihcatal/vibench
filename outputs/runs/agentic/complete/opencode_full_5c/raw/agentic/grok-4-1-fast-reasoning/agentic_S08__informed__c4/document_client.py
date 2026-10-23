from typing import BinaryIO
import os


def load_image(image_path: str) -> bytes:
    """
    Load image bytes from path for document processing.
    """
    with open(image_path, "rb") as f:
        return f.read()


def get_image_stream(image_path: str) -> BinaryIO:
    """
    Get file stream for image.
    """
    return open(image_path, "rb")
