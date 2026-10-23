"""
Generate spoken briefs for moderation reviewers using ElevenLabs Text to Speech.
"""
import os
from typing import Dict

from elevenlabs import generate, set_api_key


set_api_key(os.getenv("ELEVENLABS_API_KEY"))


def generate_reviewer_brief(text: str, voice: str = "Rachel") -> Dict:
    """Generate spoken brief for moderation reviewers."""
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    return {
        "text": text,
        "audio_bytes": audio,
        "voice": voice,
        "provider": "elevenlabs"
    }