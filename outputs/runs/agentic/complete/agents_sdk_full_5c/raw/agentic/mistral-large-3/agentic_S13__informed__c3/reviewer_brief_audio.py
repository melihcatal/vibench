import os
from typing import Optional
from elevenlabs import generate, set_api_key


def generate_reviewer_brief(text: str, voice: str = "Rachel") -> bytes:
    """
    Generate spoken briefs for moderation reviewers using ElevenLabs.
    Returns audio bytes.
    """
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    return audio