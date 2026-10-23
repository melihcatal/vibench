"""
Generate spoken briefs for moderation reviewers using ElevenLabs Text to Speech.
"""
from elevenlabs import generate, set_api_key
import os


def generate_reviewer_brief(text: str, voice_id: str = "pNInz6obpgDQGcFmaJgB") -> bytes:
    """Generate spoken brief using ElevenLabs."""
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    audio = generate(text=text, voice=voice_id, model="eleven_multilingual_v2")
    return audio