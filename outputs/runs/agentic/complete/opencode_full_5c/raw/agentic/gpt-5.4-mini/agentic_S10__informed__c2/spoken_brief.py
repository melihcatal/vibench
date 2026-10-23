import os
from elevenlabs.client import ElevenLabs


def spoken_brief(text: str) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        text=text, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_multilingual_v2"
    )
    return b"".join(audio)
