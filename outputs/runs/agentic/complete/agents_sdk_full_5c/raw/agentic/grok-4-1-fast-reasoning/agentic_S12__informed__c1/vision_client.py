import os
import base64
from typing import Optional

def image_to_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def image_to_b64(image_path: str) -> str:
    return base64.b64encode(image_to_bytes(image_path)).decode('utf-8')

def get_api_key(key_name: str) -> str:
    key = os.getenv(key_name)
    if not key:
        raise ValueError(f'Missing environment variable: {key_name}')
    return key
