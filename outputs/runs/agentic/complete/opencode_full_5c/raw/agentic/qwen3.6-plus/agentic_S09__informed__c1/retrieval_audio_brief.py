import os
from typing import List, Optional
import requests
from embeddings_models import SearchResult

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def generate_audio_brief(
    search_results: SearchResult,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    api_key: Optional[str] = None,
    output_path: Optional[str] = None,
) -> bytes:
    key = api_key or ELEVENLABS_API_KEY
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    brief_text = _build_brief_text(search_results)
    url = f"{ELEVENLABS_API_URL}/{voice_id}"
    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": brief_text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    audio_bytes = response.content
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes


def _build_brief_text(results: SearchResult) -> str:
    top_docs = results.documents[:5]
    top_scores = results.scores[:5]
    lines = ["Here are the top search results:"]
    for i, (doc, score) in enumerate(zip(top_docs, top_scores), 1):
        preview = doc[:150]
        lines.append(f"Result {i}, relevance score {score:.2f}: {preview}")
    lines.append(f"Found {len(results.documents)} total results.")
    return " ".join(lines)


def generate_audio_from_text(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    api_key: Optional[str] = None,
    output_path: Optional[str] = None,
) -> bytes:
    key = api_key or ELEVENLABS_API_KEY
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    url = f"{ELEVENLABS_API_URL}/{voice_id}"
    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    audio_bytes = response.content
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes
