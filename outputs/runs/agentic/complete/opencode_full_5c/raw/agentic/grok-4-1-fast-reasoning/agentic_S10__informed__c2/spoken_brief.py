import os
from elevenlabs import generate, set_api_key, Voice
from elevenlabs.types import VoiceSettings
from typing import Union

# Note: elevenlabs.generate returns bytes


def generate_spoken_brief(
    text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> bytes:  # Rachel voice id example
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    set_api_key(api_key)
    voice = Voice(
        voice_id=voice_id,
        settings=VoiceSettings(
            stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True
        ),
    )
    audio = generate(text=text, voice=voice, model="eleven_monolingual_v1")
    return audio
