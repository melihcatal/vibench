from __future__ import annotations

from speech_client import available_voices


def select_voice(locale: str) -> list[dict[str, str]]:
    voices = available_voices(locale)
    return [
        {"name": v.name, "locale": v.locale, "gender": v.gender or "", "description": v.description or ""}
        for v in voices
        if v.locale.lower().startswith(locale.lower())
    ]
