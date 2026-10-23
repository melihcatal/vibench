import os
from typing import Dict, Optional

PROVIDER_KEYS: Dict[str, Optional[str]] = {
    'deepl': os.getenv('DEEPL_AUTH_KEY'),
    'azure': os.getenv('AZURE_TRANSLATOR_KEY'),
    'openai': os.getenv('OPENAI_API_KEY'),
    'perspective': os.getenv('PERSPECTIVE_API_KEY'),
    'cohere': os.getenv('COHERE_API_KEY'),
}

AZURE_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')

def get_key(provider: str) -> Optional[str]:
    \"\"\"
    Get API key for a provider.
    \"\"\"
    return PROVIDER_KEYS.get(provider)

def get_azure_endpoint() -> str:
    return AZURE_ENDPOINT