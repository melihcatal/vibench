from speech_client import get_tts_client
from typing import Optional


def synthesize_ssml(
    ssml: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    client = get_tts_client()
    audio = client.generate(text=ssml, voice=voice_id, model=model_id)
    return b"".join(audio.chunks)
