from __future__ import annotations

import os

from elevenlabs.client import ElevenLabs


def generate_retrieval_audio_brief(
    results: list[dict], voice_id: str | None = None, model_id: str | None = None
) -> dict:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    selected_voice = voice_id or os.getenv(
        "ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"
    )
    selected_model = model_id or os.getenv(
        "ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2"
    )
    brief_text = " ".join(
        str(item.get("document") or item.get("text") or "") for item in results if item
    )
    audio = client.text_to_speech.convert(
        voice_id=selected_voice,
        model_id=selected_model,
        text=brief_text,
    )
    audio_bytes = b"".join(audio)
    return {
        "provider": "elevenlabs",
        "voice_id": selected_voice,
        "model_id": selected_model,
        "audio_bytes": audio_bytes,
        "text": brief_text,
    }
