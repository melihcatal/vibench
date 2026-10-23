import os
import json
from typing import List, Optional, Dict
import requests
from dashscope import tts
from dashscope.tts import TextToSpeechOptions

# Load credentials\nAPI_KEY = os.getenv('ELEVENLABS_API_KEY')
assert API_KEY, "Set ELEVENLABS_API_KEY environment variable"

VOICE_CATALOG_URL = "https://api.elevenlabs.io/v1/voices"


def list_voices() -> List[Dict]:
    """Fetch and return a list of available voices."""
    headers = {"xi-api-key": API_KEY}
    r = requests.get(VOICE_CATALOG_URL, headers=headers)
    r.raise_for_status()
    data = r.json()
    return data["voices"]


def select_voice(locale: str = "en-us", preferred_name: Optional[str] = None) -> Dict:
    """Select a voice by locale and optional name filter."""
    voices = list_voices()
    for v in voices:
        if v["locale"] == locale.lower() and (
            preferred_name is None or v["name"] == preferred_name
        ):
            return v
    raise ValueError(f"No voice found for locale {locale} with name {preferred_name}")
