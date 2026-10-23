import os
from typing import List
from translation_client import get_translation_client
from translation_models import normalize_translate_response
import requests


def generate_spoken_preview(
    translated_texts: List[str], language_code: str = "es"
) -> List[str]:
    """Generate spoken audio previews of translated copy using DashScope CosyVoice TTS.

    Returns a list of URLs (or base64 audio blobs) for each translated string.
    Requires DASHSCOPE_API_KEY environment variable.
    """
    client = get_translation_client()  # placeholder; actual TTS uses DashScope
    tts_endpoint = "https://api.dashscope.ai/v1/text-to-speech"
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY environment variable not set")
    headers = {"Authorization": f"Bearer {api_key}"}
    audio_urls = []
    for text in translated_texts:
        payload = {"model": "cosyvoice", "text": text, "language": language_code}
        resp = requests.post(tts_endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # DashScope returns a downloadable URL for the audio file
        audio_urls.append(data["url"])  # or data["audio"] if you prefer base64
    return audio_urls
