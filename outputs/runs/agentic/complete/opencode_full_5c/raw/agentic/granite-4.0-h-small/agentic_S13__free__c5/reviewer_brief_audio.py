# [LATER-STEP] reviewer_brief_audio.py
# Generate spoken briefs for moderation reviewers

import os
import openai

# Ensure OPENAI_API_KEY is set locally


def generate_audio_brief(text: str, voice: str = "alloy") -> bytes:
    """Return an .mp3 audio file (as bytes) of the provided moderation brief."""
    response = openai.Audio.synthesize(
        model="tts-1",
        input=text,
        voice=voice,
    )
    # response.audio_bytes contains the audio data
    return response.audio_bytes
