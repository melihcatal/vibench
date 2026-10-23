import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")

AUDIO_BRIEF_ENDPOINT = "https://some-tts-service/synthesize"  # placeholder


def reviewer_brief_audio(brief_text: str) -> dict:
    """Generate spoken brief for moderation reviewers.
    Returns dict containing audio URL or base64 data.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    payload = {"text": brief_text, "voice": "en-US-Standard-B"}
    resp = requests.post(AUDIO_BRIEF_ENDPOINT, json=payload)
    resp.raise_for_status()
    return resp.json()  # e.g., {"audio_url": "..."}
