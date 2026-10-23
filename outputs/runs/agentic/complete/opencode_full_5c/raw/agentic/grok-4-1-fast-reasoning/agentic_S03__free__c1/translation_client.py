import os
from typing import Dict, Any


def is_configured(provider: str) -> bool:
    keys = {
        "deepl": "DEEPL_AUTH_KEY",
        "azure": "AZURE_TRANSLATOR_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "cohere": "COHERE_API_KEY",
        "elevenlabs": "ELEVENLABS_API_KEY",
    }
    if provider in keys:
        return bool(os.getenv(keys[provider]))
    return False


def load_env(key: str) -> str:
    return os.getenv(key)
