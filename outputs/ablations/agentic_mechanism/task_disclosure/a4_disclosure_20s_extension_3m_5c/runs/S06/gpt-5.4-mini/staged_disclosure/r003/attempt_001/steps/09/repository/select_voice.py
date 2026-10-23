import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


ELEVENLABS_VOICES_URL = "https://api.elevenlabs.io/v1/voices"


def _request_voices(api_key: str) -> List[Dict[str, Any]]:
    response = requests.get(
        ELEVENLABS_VOICES_URL,
        headers={"xi-api-key": api_key, "Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    voices = payload.get("voices", []) if isinstance(payload, dict) else []
    return voices


def _voice_locale(voice: Dict[str, Any]) -> str:
    labels = voice.get("labels") or {}
    locale = labels.get("locale") or labels.get("language") or voice.get("locale") or ""
    return str(locale).strip().lower()


def _voice_name(voice: Dict[str, Any]) -> str:
    return str(voice.get("name") or voice.get("voice_id") or "").strip()


def _voice_id(voice: Dict[str, Any]) -> str:
    return str(voice.get("voice_id") or "").strip()


def select_voice(target_locale: str, voices: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    target = target_locale.strip().lower()
    exact = [v for v in voices if _voice_locale(v) == target]
    if exact:
        return exact[0]
    prefix = [v for v in voices if _voice_locale(v).startswith(target.split("-")[0])]
    if prefix:
        return prefix[0]
    return voices[0] if voices else None


def main() -> int:
    parser = argparse.ArgumentParser(description="List or select an ElevenLabs voice for a target locale")
    parser.add_argument("locale", nargs="?", help="Target locale such as en-US or fr-FR")
    parser.add_argument("--list", action="store_true", help="List all available voices")
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Missing ELEVENLABS_API_KEY", file=sys.stderr)
        return 1

    try:
        voices = _request_voices(api_key)
    except Exception as exc:
        print(f"Failed to fetch ElevenLabs voices: {exc}", file=sys.stderr)
        return 1

    if args.list:
        print(json.dumps(voices, indent=2))
        return 0

    if not args.locale:
        print("Provide a locale or use --list", file=sys.stderr)
        return 1

    voice = select_voice(args.locale, voices)
    if not voice:
        print("No voices available", file=sys.stderr)
        return 1

    result = {
        "provider": "elevenlabs",
        "target_locale": args.locale,
        "voice_id": _voice_id(voice),
        "voice_name": _voice_name(voice),
        "voice_locale": _voice_locale(voice),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
