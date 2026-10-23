import os
from typing import Dict, Optional


def get_provider_config() -> Dict[str, Optional[str]]:
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "AZURE_CONTENT_MODERATOR_KEY": os.getenv("AZURE_CONTENT_MODERATOR_KEY"),
        "AZURE_ENDPOINT": os.getenv("AZURE_ENDPOINT"),
        "PERSPECTIVE_API_KEY": os.getenv("PERSPECTIVE_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "DEEPL_API_KEY": os.getenv("DEEPL_API_KEY"),
        "COHERE_API_KEY": os.getenv("COHERE_API_KEY"),
        "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY"),
    }
