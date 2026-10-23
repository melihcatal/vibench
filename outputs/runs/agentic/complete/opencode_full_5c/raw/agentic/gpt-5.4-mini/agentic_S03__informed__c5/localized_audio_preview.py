import os
from typing import Dict

import requests


def generate_audio_preview(text: str) -> Dict[str, str]:
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{os.environ['ELEVENLABS_VOICE_ID']}",
        headers={
            "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
            "accept": "audio/mpeg",
            "content-type": "application/json",
        },
        json={"text": text, "model_id": "eleven_multilingual_v2"},
        timeout=30,
    )
    response.raise_for_status()
    return {"provider": "ElevenLabs", "audio_bytes": str(len(response.content))}
