import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_TTS_VOICE_CATALOG_URL = "https://api.openai.com/v1/audio/voices"


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}"}


def _catalog() -> List[Dict[str, Any]]:
    response = requests.get(OPENAI_TTS_VOICE_CATALOG_URL, headers=_auth_headers(), timeout=30)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict):
        for key in ("voices", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    if isinstance(payload, list):
        return payload
    return []


def _match_locale(voice: Dict[str, Any], locale: str) -> bool:
    locale = locale.lower().replace("_", "-")
    candidates = []
    for key in ("locale", "language", "lang", "locales"):
        value = voice.get(key)
        if isinstance(value, str):
            candidates.append(value.lower())
        elif isinstance(value, list):
            candidates.extend(str(v).lower() for v in value)
    return any(locale == c or c.startswith(locale) or locale.startswith(c) for c in candidates)


def select_voice(locale: str, preferred: Optional[str] = None) -> Dict[str, Any]:
    voices = _catalog()
    if preferred:
        for voice in voices:
            if str(voice.get("name", "")).lower() == preferred.lower():
                return voice
    for voice in voices:
        if _match_locale(voice, locale):
            return voice
    if voices:
        return voices[0]
    raise RuntimeError("No voices available from OpenAI voice catalog")
