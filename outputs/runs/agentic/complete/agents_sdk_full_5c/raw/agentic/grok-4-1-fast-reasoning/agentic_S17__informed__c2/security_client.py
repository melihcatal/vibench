import os
import base64
from typing import Optional

def get_kms_key_id() -> Optional[str]:
    return os.getenv('KMS_KEY_ID')

def base64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')

def base64_decode(data: str) -> bytes:
    return base64.b64decode(data)

def load_env_config() -> dict:
    return {
        'kms_key_id': os.getenv('KMS_KEY_ID'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'azure_content_safety_endpoint': os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'),
        'azure_content_safety_key': os.getenv('AZURE_CONTENT_SAFETY_KEY'),
        'cohere_api_key': os.getenv('COHERE_API_KEY'),
    }