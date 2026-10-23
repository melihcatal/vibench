import os
import json
from typing import Dict, Any, Optional

def get_secret_config() -> Dict[str, str]:
    return {
        'AWS_REGION': os.getenv('AWS_REGION', 'us-east-1'),
        'GOOGLE_CLOUD_PROJECT': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'KEY_VAULT_URL': os.getenv('KEY_VAULT_URL'),
        'VAULT_ADDR': os.getenv('VAULT_ADDR'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    }

def normalize_secret(value: str) -> Dict[str, Any]:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {'raw_value': value}