from __future__ import annotations

from typing import List, Optional

from speech_models import OPENAI_VOICE_CATALOG, VoiceOption, filter_voices_for_locale


def list_voices(locale: Optional[str] = None) -> List[VoiceOption]:
    if locale is None:
        return list(OPENAI_VOICE_CATALOG)
    return filter_voices_for_locale(locale)


def select_voice(locale: str, preferred_voice: Optional[str] = None) -> VoiceOption:
    matches = filter_voices_for_locale(locale)
    if not matches:
        raise ValueError(f"No OpenAI TTS voices available for locale: {locale}")
    if preferred_voice is not None:
        for voice in matches:
            if voice.voice_id == preferred_voice:
                return voice
    return matches[0]
