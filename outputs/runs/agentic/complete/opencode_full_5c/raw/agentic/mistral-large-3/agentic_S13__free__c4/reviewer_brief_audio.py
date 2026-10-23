from typing import Dict
import os
import requests
import base64


def generate_reviewer_brief_audio(brief_text: str) -> str:
    """
    Generates spoken briefs for moderation reviewers using ElevenLabs Text-to-Speech API.
    Model: eleven_multilingual_v2
    """
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{os.getenv('ELEVENLABS_VOICE_ID')}",
        headers={
            "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
            "Content-Type": "application/json",
        },
        json={
            "text": brief_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        },
    )
    response.raise_for_status()

    audio_file = "reviewer_brief.mp3"
    with open(audio_file, "wb") as f:
        f.write(response.content)

    return audio_file
