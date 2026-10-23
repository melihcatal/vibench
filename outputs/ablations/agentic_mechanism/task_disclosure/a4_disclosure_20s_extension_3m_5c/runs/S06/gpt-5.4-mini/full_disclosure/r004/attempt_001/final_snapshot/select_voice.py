import os
from typing import Any, Dict, List, Optional

import requests


ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"


def _api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    return key


def _headers() -> Dict[str, str]:
    return {
        "xi-api-key": _api_key(),
        "accept": "application/json",
        "content-type": "application/json",
    }


def list_voices() -> List[Dict[str, Any]]:
    response = requests.get(f"{ELEVENLABS_API_BASE}/voices", headers=_headers(), timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("voices", [])


def _locale_matches(voice: Dict[str, Any], target_locale: str) -> bool:
    locale = target_locale.strip().lower().replace("_", "-")
    labels = []
    for key in ("locale", "language", "languages"):
        value = voice.get(key)
        if isinstance(value, str):
            labels.append(value.lower())
        elif isinstance(value, list):
            labels.extend(str(item).lower() for item in value)
    labels.extend(str(voice.get("name", "")).lower().split())
    return any(locale == label or locale in label for label in labels)


def select_voice(target_locale: str, voices: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    catalog = voices if voices is not None else list_voices()
    for voice in catalog:
        if _locale_matches(voice, target_locale):
            return voice
    return catalog[0] if catalog else None
