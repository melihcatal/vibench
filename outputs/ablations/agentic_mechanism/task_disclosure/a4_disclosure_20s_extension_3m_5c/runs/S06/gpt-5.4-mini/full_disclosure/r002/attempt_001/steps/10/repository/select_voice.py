import os
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI


@dataclass(frozen=True)
class VoiceOption:
    name: str
    locale: str
    description: str = ""


_OPENAI_VOICES: List[VoiceOption] = [
    VoiceOption(name="alloy", locale="en"),
    VoiceOption(name="echo", locale="en"),
    VoiceOption(name="fable", locale="en-GB"),
    VoiceOption(name="onyx", locale="en"),
    VoiceOption(name="nova", locale="en-US"),
    VoiceOption(name="shimmer", locale="en-US"),
]


def _normalize_locale(locale: str) -> str:
    return locale.replace("_", "-").strip().lower()


def _locale_score(voice_locale: str, target_locale: str) -> int:
    voice_locale = _normalize_locale(voice_locale)
    target_locale = _normalize_locale(target_locale)
    if voice_locale == target_locale:
        return 3
    if voice_locale.split("-")[0] == target_locale.split("-")[0]:
        return 2
    if target_locale.startswith(voice_locale) or voice_locale.startswith(target_locale):
        return 1
    return 0


def list_voices(target_locale: str, api_key: Optional[str] = None) -> List[VoiceOption]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    client.models.list()
    normalized = _normalize_locale(target_locale)
    return sorted(_OPENAI_VOICES, key=lambda v: (_locale_score(v.locale, normalized), v.name), reverse=True)


def select_voice(target_locale: str, api_key: Optional[str] = None) -> str:
    voices = list_voices(target_locale, api_key=api_key)
    if not voices:
        raise ValueError("No voices available")
    return voices[0].name
