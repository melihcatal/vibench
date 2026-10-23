from __future__ import annotations

from typing import List, Optional

from speech_client import create_polly_client, list_voices, load_config, select_voice_for_locale
from speech_models import VoiceOption


def select_voice(locale: str, voice_name: Optional[str] = None) -> VoiceOption:
    client = create_polly_client(load_config())
    if voice_name:
        voices: List[VoiceOption] = list_voices(client, locale=locale)
        for voice in voices:
            if voice.name == voice_name:
                return voice
    selected = select_voice_for_locale(client, locale)
    if selected is None:
        raise ValueError(f"No Amazon Polly voice found for locale: {locale}")
    return selected
