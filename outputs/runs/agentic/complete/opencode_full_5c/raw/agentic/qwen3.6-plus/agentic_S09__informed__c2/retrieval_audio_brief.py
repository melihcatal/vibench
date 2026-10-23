import os
import requests


ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


def generate_audio_brief(search_results, voice_id=None):
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    voice_id = voice_id or ELEVENLABS_VOICE_ID

    brief_text = _build_brief_text(search_results)

    url = f"{ELEVENLABS_TTS_URL}/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": brief_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.content


def _build_brief_text(search_results):
    lines = ["Here are your search results:"]
    for i, result in enumerate(search_results, 1):
        doc = result.get("document", "N/A")
        score = result.get("similarity", 0.0)
        lines.append(f"Result {i}: {doc} with a relevance score of {score:.2f}.")
    return " ".join(lines)
