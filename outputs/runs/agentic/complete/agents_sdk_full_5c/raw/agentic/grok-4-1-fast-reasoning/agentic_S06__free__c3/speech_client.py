import os
from typing import Dict, List

# Local configuration for Text-to-Speech
GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
DEFAULT_LANGUAGE_CODE: str = "en-US"
VOICE_MAP: Dict[str, str] = {
    "en-US": "en-US-Standard-A",
    "en-GB": "en-GB-Standard-A",
    "es-ES": "es-ES-Standard-A",
    "fr-FR": "fr-FR-Standard-A",
}

def get_default_voice(language_code: str) -> str:
    """Get default voice for locale."""
    return VOICE_MAP.get(language_code, "en-US-Standard-A")

def supported_languages() -> List[str]:
    """List supported languages."""
    return list(VOICE_MAP.keys())
