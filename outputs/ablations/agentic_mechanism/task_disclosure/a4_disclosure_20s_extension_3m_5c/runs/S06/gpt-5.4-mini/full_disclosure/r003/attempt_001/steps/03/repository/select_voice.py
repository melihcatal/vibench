import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


@dataclass
class VoiceOption:
    name: str
    locale: str


def _normalize_locale(locale: str) -> str:
    return locale.strip().lower().replace("_", "-")


def _openai_tts_voices() -> List[VoiceOption]:
    return [
        VoiceOption("alloy", "en"),
        VoiceOption("echo", "en"),
        VoiceOption("fable", "en-gb"),
        VoiceOption("onyx", "en"),
        VoiceOption("nova", "en"),
        VoiceOption("shimmer", "en"),
    ]


def list_voices(target_locale: Optional[str] = None) -> List[Dict[str, str]]:
    voices = _openai_tts_voices()
    if target_locale:
        locale = _normalize_locale(target_locale)
        filtered = [v for v in voices if v.locale == locale or v.locale.split("-")[0] == locale.split("-")[0]]
    else:
        filtered = voices
    return [{"name": v.name, "locale": v.locale} for v in filtered]


def select_voice(target_locale: str) -> Dict[str, str]:
    locale = _normalize_locale(target_locale)
    voices = _openai_tts_voices()
    for voice in voices:
        if voice.locale == locale or voice.locale.split("-")[0] == locale.split("-")[0]:
            return {"name": voice.name, "locale": voice.locale, "provider": "openai"}
    return {"name": voices[0].name, "locale": voices[0].locale, "provider": "openai"}


def _openai_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def fetch_openai_voice_selection(target_locale: str) -> Dict[str, Any]:
    headers = _openai_headers()
    payload = {"target_locale": _normalize_locale(target_locale), "voices": OPENAI_TTS_VOICES}
    response = requests.post("https://api.openai.com/v1/voices/select", headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
