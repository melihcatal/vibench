from __future__ import annotations

import os
from typing import Any, Dict

from elevenlabs import ElevenLabs


ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"


def localized_audio_preview(
    text: str, voice_id: str, output_format: str = "mp3_44100_128"
) -> Dict[str, Any]:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=ELEVENLABS_MODEL_ID,
        text=text,
        output_format=output_format,
    )
    audio_bytes = b"".join(audio)
    return {
        "provider": "ElevenLabs",
        "model": ELEVENLABS_MODEL_ID,
        "voice_id": voice_id,
        "audio": audio_bytes,
        "content_type": "audio/mpeg"
        if output_format.startswith("mp3")
        else "application/octet-stream",
    }
