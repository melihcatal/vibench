from __future__ import annotations

from model_client import DEFAULT_TTS_MODEL, get_openai_client
from model_models import AudioSpeechResult


def generate_spoken_brief(text: str, voice: str = "alloy") -> AudioSpeechResult:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=voice,
        input=text,
        format="mp3",
    )
    return AudioSpeechResult(
        audio_bytes=response.read(),
        model=DEFAULT_TTS_MODEL,
        voice=voice,
    )
