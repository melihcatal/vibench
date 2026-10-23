import os
import base64
import mimetypes
from typing import Tuple


def load_document(image_path: str) -> Tuple[bytes, str]:
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        if image_path.lower().endswith(".pdf"):
            mime_type = "application/pdf"
        else:
            mime_type = "image/jpeg"
    with open(image_path, "rb") as f:
        return f.read(), mime_type
