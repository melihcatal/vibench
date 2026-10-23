from typing import Dict
from safety_models import ReviewerBriefAudio
from elevenlabs import generate, set_api_key
import os


def generate_reviewer_brief(text: str) -> ReviewerBriefAudio:
    """Generate spoken briefs for moderation reviewers using ElevenLabs TTS."""
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))

    audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    return ReviewerBriefAudio(
        audio_content=audio,
        text_content=text,
        duration_seconds=len(audio) / 16000,  # Approximate duration
    )
