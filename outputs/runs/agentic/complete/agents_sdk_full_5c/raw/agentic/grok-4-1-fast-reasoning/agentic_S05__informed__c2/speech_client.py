import os
from typing import Dict, Any, Optional

def get_speech_config(provider: str) -> Dict[str, Any]:
    configs = {
        'deepgram': {'api_key': os.getenv('DEEPGRAM_API_KEY')},
        'google': {'credentials_path': os.getenv('GOOGLE_APPLICATION_CREDENTIALS')},
        'azure': {
            'key': os.getenv('AZURE_SPEECH_KEY'),
            'region': os.getenv('AZURE_SPEECH_REGION')
        },
    }
    return configs.get(provider, {})