import os
from typing import Optional

from elevenlabs.client import ElevenLabs


def synthesize_text(text: str, voice: Optional[str] = None, model: str = "eleven_turbo_v2_5") -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    voice_id = voice or os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    audio = client.text_to_speech.convert(text=text, voice_id=voice_id, model_id=model)
    if isinstance(audio, (bytes, bytearray)):
        return bytes(audio)
    return b"".join(chunk for chunk in audio)
