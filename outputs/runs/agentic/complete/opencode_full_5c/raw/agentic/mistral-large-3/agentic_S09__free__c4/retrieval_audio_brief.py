from typing import List, Dict
import requests
import os
import base64


def retrieval_audio_brief(results: List[Dict], output_file: str = "brief.mp3") -> str:
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_LABS_API_KEY environment variable not set")

    brief_text = "Here are the top results:\n"
    for idx, result in enumerate(results[:3], 1):
        brief_text += f"Result {idx}: {result.get('text', 'No text available')}\n"

    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }
    payload = {
        "text": brief_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"ElevenLabs API request failed: {response.text}")

    with open(output_file, "wb") as f:
        f.write(response.content)

    return output_file
