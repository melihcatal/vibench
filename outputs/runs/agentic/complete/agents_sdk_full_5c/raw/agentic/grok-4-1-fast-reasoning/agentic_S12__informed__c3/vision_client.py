import base64
from typing import Optional

def image_to_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def image_to_base64(image_path: str) -> str:
    return base64.b64encode(image_to_bytes(image_path)).decode('utf-8')