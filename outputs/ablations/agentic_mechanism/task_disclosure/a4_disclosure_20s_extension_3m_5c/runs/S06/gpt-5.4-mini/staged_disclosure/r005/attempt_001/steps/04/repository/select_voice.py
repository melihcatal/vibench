import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    return {"xi-api-key": api_key, "Content-Type": "application/json"}


def _get_voices() -> List[Dict[str, Any]]:
    response = requests.get(f"{ELEVENLABS_API_BASE}/voices", headers=_headers(), timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("voices", [])


def _voice_locale_match(voice: Dict[str, Any], target_locale: str) -> bool:
    labels = []
    for key in ("labels", "language", "locale"):
        value = voice.get(key)
        if isinstance(value, dict):
            labels.extend(str(v).lower() for v in value.values())
        elif isinstance(value, list):
            labels.extend(str(v).lower() for v in value)
        elif value:
            labels.append(str(value).lower())
    name = str(voice.get("name", "")).lower()
    target = target_locale.lower()
    return any(target in item or item in target for item in labels) or target in name


def list_voices(target_locale: str) -> List[Dict[str, Any]]:
    return [voice for voice in _get_voices() if _voice_locale_match(voice, target_locale)]


def select_voice(target_locale: str) -> Optional[Dict[str, Any]]:
    voices = list_voices(target_locale)
    if not voices:
        return None
    return voices[0]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: select_voice.py <locale> [--list]", file=sys.stderr)
        return 1

    target_locale = sys.argv[1]
    voices = list_voices(target_locale)

    if len(sys.argv) > 2 and sys.argv[2] == "--list":
        print(json.dumps(voices, indent=2))
        return 0

    selected = voices[0] if voices else None
    print(json.dumps(selected, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
