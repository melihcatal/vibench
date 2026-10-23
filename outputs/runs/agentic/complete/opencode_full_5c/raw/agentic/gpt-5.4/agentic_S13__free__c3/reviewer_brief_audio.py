from __future__ import annotations

from typing import Dict

from safety_client import ELEVENLABS_TTS_API_URL, default_session, elevenlabs_api_key


def reviewer_brief_audio(
    text: str,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
) -> Dict[str, str | bytes]:
    response = default_session().post(
        f"{ELEVENLABS_TTS_API_URL}/{voice_id}",
        headers={
            "xi-api-key": elevenlabs_api_key(),
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": model_id,
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
        },
        timeout=60,
    )
    response.raise_for_status()
    return {
        "audio_bytes": response.content,
        "content_type": response.headers.get("Content-Type", "audio/mpeg"),
        "provider": "elevenlabs",
        "model": model_id,
    }
