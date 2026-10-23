from __future__ import annotations

from typing import List, Optional

from speech_client import list_azure_voices
from speech_models import VoiceOption


def select_voice(locale: str, preferred_prefix: Optional[str] = None) -> List[VoiceOption]:
    voices = list_azure_voices(locale)
    if preferred_prefix:
        preferred = [voice for voice in voices if voice.name.startswith(preferred_prefix)]
        if preferred:
            return preferred
    return voices
