import os
from typing import List, Dict
import requests


def generate_spoken_brief(retrieved_results: List[Dict[str, str]]) -> bytes:
    """Generate a spoken brief from retrieved search results using ElevenLabs API."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    brief_text = "Here are the top results:\n"
    for idx, result in enumerate(retrieved_results, 1):
        brief_text += f"Result {idx}: {result.get('text', '')}\n"
    
    payload = {
        "text": brief_text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error: {response.text}")
    
    return response.content