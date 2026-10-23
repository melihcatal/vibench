from typing import Dict
import os
import requests
import base64


def generate_reviewer_brief_audio(brief_text: str) -> str:
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Predefined voice ID for Eleven Labs
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    data = {
        "text": brief_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    audio_file_path = "/tmp/reviewer_brief.mp3"
    with open(audio_file_path, "wb") as f:
        f.write(response.content)

    return audio_file_path
