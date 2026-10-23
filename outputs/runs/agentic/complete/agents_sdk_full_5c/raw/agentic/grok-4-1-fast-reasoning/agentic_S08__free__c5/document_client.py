import os
import base64
from typing import Optional

def image_bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

def get_google_cloud_project() -> str:
    return os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id')

def get_aws_region() -> str:
    return os.getenv('AWS_REGION', 'us-east-1')