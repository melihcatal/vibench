from __future__ import annotations

import os
from typing import Any, Dict

from elevenlabs import ElevenLabs


def generate_platform_brief_audio(
    text: str, voice_id: str | None = None
) -> Dict[str, Any]:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)
    chosen_voice = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
    audio = client.text_to_speech.convert(
        voice_id=chosen_voice,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return {
        "provider": "elevenlabs",
        "voice_id": chosen_voice,
        "model_id": "eleven_multilingual_v2",
        "audio": audio_bytes,
        "content_type": "audio/mpeg",
    }
