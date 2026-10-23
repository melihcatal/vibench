import requests
from safety_client import get_api_key


def reviewer_brief_audio(brief: str) -> bytes:
    api_key = get_api_key("ELEVENLABS_API_KEY")
    voice_id = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }
    data = {
        "text": brief,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.content
