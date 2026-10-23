from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import texttospeech

DEFAULT_LOCALE = os.getenv("GOOGLE_CLOUD_TTS_LOCALE", "en-US")
DEFAULT_VOICE = os.getenv("GOOGLE_CLOUD_TTS_VOICE", "en-US-Neural2-D")


@lru_cache(maxsize=1)
def build_speech_client() -> texttospeech.TextToSpeechClient:
    """Construct a cached Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()


def default_voice_name(locale: Optional[str] = None) -> str:
    if locale == "en-GB":
        return os.getenv("GOOGLE_CLOUD_TTS_VOICE_EN_GB", "en-GB-Neural2-B")
    return DEFAULT_VOICE
