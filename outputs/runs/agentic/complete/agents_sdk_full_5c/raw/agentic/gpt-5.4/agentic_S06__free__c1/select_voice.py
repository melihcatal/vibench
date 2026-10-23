from __future__ import annotations

from typing import List, Optional

from speech_client import build_session
from speech_models import VoiceSelection, locale_matches, voice_from_api


ELEVENLABS_VOICES_PATH = "/voices"


def list_voices(locale: Optional[str] = None) -> List[VoiceSelection]:
    session, config = build_session()
    response = session.get(f"{config.base_url}{ELEVENLABS_VOICES_PATH}", timeout=config.timeout)
    response.raise_for_status()
    voices = response.json().get("voices", [])
    return [voice_from_api(v) for v in voices if locale_matches(locale, v)]


def select_voice(locale: str, preferred_name: Optional[str] = None) -> VoiceSelection:
    voices = list_voices(locale=locale)
    if not voices:
        raise LookupError(f"No ElevenLabs voice found for locale {locale}")
    if preferred_name:
        for voice in voices:
            if voice.name.lower() == preferred_name.lower():
                return voice
    return voices[0]
