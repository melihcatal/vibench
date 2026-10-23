from __future__ import annotations

import os
from typing import Any, Dict

from elevenlabs import ElevenLabs


ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"


def generate_platform_brief_audio(text: str, voice_id: str) -> Dict[str, Any]:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_44100_128",
        text=text,
        model_id=ELEVENLABS_MODEL_ID,
    )
    audio_bytes = b"".join(audio)
    return {
        "provider": "ElevenLabs",
        "model": ELEVENLABS_MODEL_ID,
        "voice_id": voice_id,
        "audio_bytes": audio_bytes,
        "content_type": "audio/mpeg",
    }
