import base64
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
ELEVENLABS_MODEL_ID = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def build_reviewer_brief_text(review_items: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = ["Moderator reviewer brief."]
    for index, item in enumerate(review_items, start=1):
        label = item.get("label") or item.get("decision") or "item"
        summary = item.get("summary") or item.get("text") or "No summary provided."
        action = item.get("action") or item.get("recommendation") or "review"
        lines.append(f"{index}. {label}: {summary} Recommended action: {action}.")
    return " ".join(lines)


def generate_spoken_brief(review_items: Iterable[Dict[str, Any]]) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")

    text = build_reviewer_brief_text(review_items)
    response = requests.post(
        f"{ELEVENLABS_API_URL}/{ELEVENLABS_VOICE_ID}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        json={
            "text": text,
            "model_id": ELEVENLABS_MODEL_ID,
            "output_format": "mp3_44100_128",
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.content


def generate_spoken_brief_base64(review_items: Iterable[Dict[str, Any]]) -> str:
    return base64.b64encode(generate_spoken_brief(review_items)).decode("ascii")
