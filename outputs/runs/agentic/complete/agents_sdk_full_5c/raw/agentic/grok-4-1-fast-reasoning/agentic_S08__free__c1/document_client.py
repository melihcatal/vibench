import os
import base64
from typing import Union

def get_google_cloud_project() -> str:
    return os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id')

def get_aws_region() -> str:
    return os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

def image_to_base64(image_bytes: bytes, mime_type: str = 'image/png') -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

def prepare_raw_document(image_bytes: bytes, mime_type: str = 'image/png') -> dict:
    return {
        'content': image_bytes,
        'mime_type': mime_type
    }
