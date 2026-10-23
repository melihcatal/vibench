import os
from elevenlabs.client import ElevenLabs


def spoken_brief(text: str) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id="Rachel",
        model_id="eleven_multilingual_v2",
        text=text,
    )
    return b"".join(audio)
