import os
from safety_client import get_client
from safety_models import ModerationRequest, moderate_text

# LATER-STEP
# Generate a spoken brief for moderation reviewers using text-to-speech.
# Provider identification: ELEVENLABS (ElevenLabs Text-to-Speech)


def generate_audio_brief(reason: str, voice_id: str = "violet-1") -> bytes:
    """
    Returns audio bytes for a moderation reviewer brief.
    """
    client = get_client("elevenlabs")
    if client is None:
        raise RuntimeError("ElevenLabs client not configured")
    audio = client.text_to_speech(
        text=reason,
        voice_id=voice_id,
        model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_monolingual_v1"),
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.85,
        },
    )
    return audio.audio  # assumes the SDK returns an object with .audio bytes
