import base64
import os

def load_image(image_path: str) -> bytes:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    with open(image_path, 'rb') as f:
        return f.read()