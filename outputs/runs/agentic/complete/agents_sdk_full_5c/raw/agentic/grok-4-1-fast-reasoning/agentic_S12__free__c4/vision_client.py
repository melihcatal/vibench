import os
import base64
from typing import Dict, Any

def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def image_to_base64(image_path: str) -> str:
    img_bytes = load_image_bytes(image_path)
    return base64.b64encode(img_bytes).decode('utf-8')

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_IMAGE_BUCKET = os.getenv('S3_IMAGE_BUCKET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')