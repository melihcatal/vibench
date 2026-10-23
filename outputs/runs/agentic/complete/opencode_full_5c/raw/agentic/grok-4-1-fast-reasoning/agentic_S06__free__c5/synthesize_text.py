from speech_client import get_tts_client
from typing import Optional


def synthesize_text(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel
    model_id: Optional[str] = "eleven_turbo_v2",
) -> bytes:
    client = get_tts_client()
    audio = client.generate(text=text, voice=voice_id, model=model_id)
    return b"".join(audio.chunks)
