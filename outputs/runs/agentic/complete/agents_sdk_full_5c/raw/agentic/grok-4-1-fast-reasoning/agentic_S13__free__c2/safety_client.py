import os
from typing import Dict, Any

def get_safety_config() -> Dict[str, Any]:
    """Local configuration loader for Text Content Safety providers."""
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'sightengine': {
            'api_user': os.getenv('SIGHTENGINE_API_USER'),
            'api_secret': os.getenv('SIGHTENGINE_API_SECRET'),
        },
        'perspective_api_key': os.getenv('PERSPECTIVE_API_KEY'),
    }

def normalize_text(text: str) -> str:
    """Normalize input text for moderation."""
    return text.strip()
