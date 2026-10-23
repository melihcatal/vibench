import os
import sys
import json
from typing import Any, Dict, List, Optional

import requests

ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"
ELEVENLABS_VOICES_ENDPOINT = f"{ELEVENLABS_API_BASE}/voices"


def _load_voices(api_key: str) -> List[Dict[str, Any]]:
    headers = {"xi-api-key": api_key}
    response = requests.get(ELEVENLABS_VOICES_ENDPOINT, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    voices = payload.get("voices", []) if isinstance(payload, dict) else []
    return voices


def _normalize_locale(locale: str) -> str:
    return locale.strip().lower().replace("_", "-")


def _voice_locales(voice: Dict[str, Any]) -> List[str]:
    locales: List[str] = []
    labels = voice.get("labels")
    if isinstance(labels, dict):
        for key in ("language", "locale", "spoken_language", "accent"):
            value = labels.get(key)
            if isinstance(value, str) and value.strip():
                locales.append(_normalize_locale(value))
    category = voice.get("category")
    if isinstance(category, str) and category.strip():
        locales.append(_normalize_locale(category))
    name = voice.get("name")
    if isinstance(name, str) and name.strip():
        locales.append(_normalize_locale(name))
    return locales


def select_voice(target_locale: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    target = _normalize_locale(target_locale)
    voices = _load_voices(api_key)
    if not voices:
        raise RuntimeError("No voices returned by ElevenLabs")
    exact_matches = []
    partial_matches = []
    for voice in voices:
        locales = _voice_locales(voice)
        if target in locales:
            exact_matches.append(voice)
        elif any(target.split("-")[0] == loc.split("-")[0] for loc in locales if loc):
            partial_matches.append(voice)
    candidates = exact_matches or partial_matches or voices
    return candidates[0]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: select_voice.py LOCALE")
    voice = select_voice(sys.argv[1])
    print(json.dumps(voice, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

