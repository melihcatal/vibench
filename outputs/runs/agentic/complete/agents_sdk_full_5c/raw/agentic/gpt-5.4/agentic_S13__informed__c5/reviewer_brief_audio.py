from __future__ import annotations

import io
import os
from typing import Dict

from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> Dict[str, object]:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        text=text,
    )
    buffer = io.BytesIO()
    for chunk in audio_stream:
        if chunk:
            buffer.write(chunk)
    audio_bytes = buffer.getvalue()
    return {
        "provider": "elevenlabs",
        "voice_id": voice_id,
        "model_id": "eleven_multilingual_v2",
        "audio_bytes": audio_bytes,
        "content_type": "audio/mpeg",
        "size": len(audio_bytes),
    }
