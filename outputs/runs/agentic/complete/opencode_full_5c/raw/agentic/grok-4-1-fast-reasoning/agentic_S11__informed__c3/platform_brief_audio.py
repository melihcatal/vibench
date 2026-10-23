import os
import requests


def generate_platform_brief_audio(
    text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }
    resp = requests.post(url, json=data, headers=headers)
    if resp.status_code == 200:
        return resp.content
    else:
        raise ValueError(f"ElevenLabs API error: {resp.status_code}")
