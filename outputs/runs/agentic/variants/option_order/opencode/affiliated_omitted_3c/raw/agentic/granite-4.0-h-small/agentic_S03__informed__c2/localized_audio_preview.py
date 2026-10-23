import os
import json
import requests
from typing import List, Dict

# Text-to-Speech example: ElevenLabs Text to Speech (REST API)
# Uses the public ElevenLabs API for spoken previews


def generate_audio_previews(utterances: List[str]) -> List[Dict[str, Any]]:
    """Produce spoken audio previews for each translated utterance using ElevenLabs.

    Args:
        utterances: List of translated text strings.

    Returns:
        List of dicts with 'utterance', 'audio_url' and any metadata.
    """
    # ElevenLabs API credentials from env vars
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY environment variable not set")

    base_url = "https://api.elevenlabs.io/v1/text-to-speech/"  # placeholder endpoint
    # For demo we use a generic public endpoint; real deployment should use appropriate model ID
    model_id = "eleven_multilingual_v1"

    previews = []
    for idx, text in enumerate(utterances):
        headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {"stability": 0.75, "similarity_boost": 0.85},
        }
        response = requests.post(
            base_url + model_id, json=payload, headers=headers, timeout=15
        )
        if response.status_code != 200:
            raise RuntimeError(f"ElevenLabs API error: {response.text}")
        data = response.json()
        # The response contains a URL to the generated audio file
        audio_url = data.get("audio_url")
        previews.append(
            {
                "utterance": text,
                "audio_url": audio_url,
                "model": model_id,
                "status": "ok",
            }
        )
    return previews


# Example usage when run directly (requires ELEVENLABS_API_KEY)
if __name__ == "__main__":
    samples = ["Bonjour, comment ça va?", "Good morning!"]
    for entry in generate_audio_previews(samples):
        print(entry)
