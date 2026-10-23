import os
import base64

def load_image(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

def get_google_project() -> str:
    return os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id')

def get_aws_region() -> str:
    return os.getenv('AWS_REGION', 'us-east-1')