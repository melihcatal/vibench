import base64
import os

def get_image_bytes(image_path: str) -> bytes:
    if image_path.startswith(('http://', 'https://')):
        import requests
        response = requests.get(image_path)
        response.raise_for_status()
        return response.content
    else:
        with open(image_path, 'rb') as image_file:
            return image_file.read()

def encode_image_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('latin1')