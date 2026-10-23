from __future__ import annotations

import requests

from safety_client import get_openai_base_url, get_openai_headers
from safety_models import AudioBriefResult


TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICE = "alloy"


def reviewer_brief_audio(brief_text: str, audio_format: str = "mp3") -> AudioBriefResult:
    response = requests.post(
        f"{get_openai_base_url()}/audio/speech",
        headers=get_openai_headers(),
        json={
            "model": TTS_MODEL,
            "voice": TTS_VOICE,
            "input": brief_text,
            "format": audio_format,
        },
        timeout=60,
    )
    response.raise_for_status()
    return AudioBriefResult(
        audio_base64=response.content.decode("utf-8"),
        format=audio_format,
        provider="OpenAI",
        voice=TTS_VOICE,
    )
