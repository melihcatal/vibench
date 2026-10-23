import os
import requests


def reviewer_brief_audio(
    brief_text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    output_path: str = "reviewer_brief.mp3",
) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    data = {
        "text": brief_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path
