# Local configuration and client helper utilities for Text-to-Speech

import os
from typing import Dict, Any

TTS_DEFAULTS: Dict[str, Any] = {
    "language_code": "en-US",
    "voice_name": "en-US-Neural2-I",
    "speaking_rate": 1.0,
    "audio_encoding": "MP3",
}

def get_credentials_info() -> Dict[str, str]:
    path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable must be set.")
    return {"credentials_path": path}
