import os
import io
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from typing import Optional

def localized_audio_preview(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY required")
    client = ElevenLabs(api_key=api_key)
    stream = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_monolingual_v1",
        stream=True
    )
    buffer = io.BytesIO()
    for chunk in stream:
        buffer.write(chunk)
    buffer.seek(0)
    return buffer.getvalue()