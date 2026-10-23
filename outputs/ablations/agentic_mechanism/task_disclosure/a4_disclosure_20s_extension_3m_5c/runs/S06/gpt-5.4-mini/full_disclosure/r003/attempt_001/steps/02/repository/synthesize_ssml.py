import base64
import os
from typing import Any, Dict, Optional

import requests


def synthesize_ssml(ssml: str, voice_name: str, speaking_rate: float = 1.0, pitch: str = "0st") -> bytes:
    api_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not api_key:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS is required for Google Cloud Text-to-Speech")
    endpoint = "https://texttospeech.googleapis.com/v1/text:synthesize"
    payload: Dict[str, Any] = {
        "input": {"ssml": ssml},
        "voice": {"languageCode": "en-US", "name": voice_name},
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": speaking_rate, "pitch": pitch},
    }
    response = requests.post(endpoint, json=payload, timeout=60)
    response.raise_for_status()
    audio_content = response.json()["audioContent"]
    return base64.b64decode(audio_content)
