from __future__ import annotations

from model_client import DEFAULT_AUDIO_MODEL, DEFAULT_VOICE, get_openai_client
from model_models import SpeechResult


def generate_spoken_brief(
    text: str, voice: str | None = None, model: str | None = None
) -> SpeechResult:
    client = get_openai_client()
    selected_voice = voice or DEFAULT_VOICE
    selected_model = model or DEFAULT_AUDIO_MODEL
    response = client.audio.speech.create(
        model=selected_model,
        voice=selected_voice,
        input=text,
        format="mp3",
    )
    return SpeechResult(
        provider="openai",
        audio_bytes=response.read(),
        content_type="audio/mpeg",
        voice_id=selected_voice,
    )
