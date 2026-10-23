import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}"}


def list_voices() -> List[Dict[str, Any]]:
    response = requests.get(f"{OPENAI_API_BASE}/audio/voices", headers=_auth_headers(), timeout=30)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict) and "data" in payload and isinstance(payload["data"], list):
        return payload["data"]
    if isinstance(payload, list):
        return payload
    raise RuntimeError("Unexpected voice list response format")


def select_voice(target_locale: str, voices: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    target = target_locale.strip().lower().replace("_", "-")
    candidates = voices if voices is not None else list_voices()
    exact = []
    prefix = []
    fallback = []
    for voice in candidates:
        locale = str(voice.get("locale", "")).strip().lower().replace("_", "-")
        if not locale:
            fallback.append(voice)
        elif locale == target:
            exact.append(voice)
        elif locale.startswith(target.split("-")[0]):
            prefix.append(voice)
        elif target.startswith(locale.split("-")[0]):
            prefix.append(voice)
    if exact:
        return exact[0]
    if prefix:
        return prefix[0]
    if fallback:
        return fallback[0]
    raise LookupError(f"No voice found for locale: {target_locale}")


__all__ = ["list_voices", "select_voice"]
