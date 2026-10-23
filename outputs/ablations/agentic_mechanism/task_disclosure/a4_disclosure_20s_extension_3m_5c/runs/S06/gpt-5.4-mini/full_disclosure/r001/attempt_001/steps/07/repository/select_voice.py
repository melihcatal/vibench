from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests


OPENAI_VOICES_URL = "https://api.openai.com/v1/audio/voices"


@dataclass(frozen=True)
class VoiceOption:
    name: str
    locale: Optional[str] = None
    gender: Optional[str] = None
    description: Optional[str] = None


def _normalize_locale(value: Optional[str]) -> str:
    return (value or "").strip().lower().replace("_", "-")


def _voice_matches_locale(voice: VoiceOption, target_locale: str) -> bool:
    locale = _normalize_locale(voice.locale)
    target = _normalize_locale(target_locale)
    if not locale or not target:
        return False
    return locale == target or locale.startswith(f"{target}-") or target.startswith(f"{locale}-")


def _rank_voice_candidates(voices: Iterable[VoiceOption], target_locale: str) -> List[VoiceOption]:
    exact: List[VoiceOption] = []
    partial: List[VoiceOption] = []
    for voice in voices:
        if _voice_matches_locale(voice, target_locale):
            if _normalize_locale(voice.locale) == _normalize_locale(target_locale):
                exact.append(voice)
            else:
                partial.append(voice)
    return exact + partial


def _openai_voice_catalog(api_key: Optional[str] = None) -> List[VoiceOption]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.get(
        OPENAI_VOICES_URL,
        headers={"Authorization": f"Bearer {key}"},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    items = payload.get("data", payload if isinstance(payload, list) else [])
    voices: List[VoiceOption] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        voices.append(
            VoiceOption(
                name=str(item.get("name") or item.get("voice") or ""),
                locale=item.get("locale") or item.get("language") or item.get("languages", [None])[0],
                gender=item.get("gender"),
                description=item.get("description"),
            )
        )
    return [voice for voice in voices if voice.name]


def select_voice(target_locale: str, api_key: Optional[str] = None, voices: Optional[Iterable[VoiceOption]] = None) -> VoiceOption:
    catalog = list(voices) if voices is not None else _openai_voice_catalog(api_key=api_key)
    ranked = _rank_voice_candidates(catalog, target_locale)
    if not ranked:
        raise ValueError(f"No voice found for locale: {target_locale}")
    return ranked[0]


def list_voices_for_locale(target_locale: str, api_key: Optional[str] = None, voices: Optional[Iterable[VoiceOption]] = None) -> List[VoiceOption]:
    catalog = list(voices) if voices is not None else _openai_voice_catalog(api_key=api_key)
    return _rank_voice_candidates(catalog, target_locale)
