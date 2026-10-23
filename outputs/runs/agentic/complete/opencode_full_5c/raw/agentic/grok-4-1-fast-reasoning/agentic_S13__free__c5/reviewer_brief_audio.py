import os
from elevenlabs import generate
from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(brief_text: str) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = generate(text=brief_text, voice="Rachel", model="eleven_monolingual_v1")
    return audio
