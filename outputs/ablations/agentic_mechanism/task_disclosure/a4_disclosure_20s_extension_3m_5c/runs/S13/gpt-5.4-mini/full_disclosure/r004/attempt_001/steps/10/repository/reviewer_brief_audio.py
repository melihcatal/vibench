import base64
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_AUDIO_MODEL = os.getenv("OPENAI_REVIEWER_BRIEF_AUDIO_MODEL", "gpt-4.1-mini-tts")


def _resolve_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def _build_brief_prompt(review_items: List[Dict[str, Any]]) -> str:
    return (
        "Create a spoken moderation reviewer brief. "
        "Keep it concise, factual, and suitable for audio playback. "
        "Mention the highest-priority risks first, then any notable patterns, "
        f"and end with a short review recommendation. Items: {review_items}"
    )


def generate_reviewer_brief_audio(review_items: List[Dict[str, Any]], api_key: Optional[str] = None, model: Optional[str] = None, voice: str = "alloy") -> Dict[str, Any]:
    if not isinstance(review_items, list):
        raise TypeError("review_items must be a list")
    if any(not isinstance(item, dict) for item in review_items):
        raise TypeError("each review item must be a dictionary")

    key = _resolve_api_key(api_key)
    audio_model = model or OPENAI_AUDIO_MODEL
    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": audio_model,
            "input": [
                {
                    "role": "system",
                    "content": "You generate clear spoken briefs for moderation reviewers.",
                },
                {
                    "role": "user",
                    "content": _build_brief_prompt(review_items),
                },
            ],
            "audio": {"voice": voice, "format": "mp3"},
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    audio_b64 = ""
    text_brief = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "audio":
                audio_b64 = content.get("audio", "") or content.get("data", "")
            if content.get("type") == "output_text":
                text_brief = content.get("text", "")
    audio_bytes = base64.b64decode(audio_b64) if audio_b64 else b""
    return {
        "provider": "openai",
        "model": audio_model,
        "voice": voice,
        "brief_text": text_brief,
        "audio_bytes": audio_bytes,
        "raw": data,
    }
