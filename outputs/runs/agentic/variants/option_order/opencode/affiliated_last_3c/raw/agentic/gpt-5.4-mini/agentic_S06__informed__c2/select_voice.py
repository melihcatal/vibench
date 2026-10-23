from typing import List, Optional

from speech_client import list_voices
from speech_models import VoiceOption, voice_option_from_sdk


def select_voice(
    locale: str = None, preferred_name: str = None
) -> Optional[VoiceOption]:
    voices = list_voices(locale)
    options = [voice_option_from_sdk(v) for v in voices]
    if preferred_name:
        for option in options:
            if option.name == preferred_name:
                return option
    return options[0] if options else None


def list_voice_options(locale: str = None) -> List[VoiceOption]:
    return [voice_option_from_sdk(v) for v in list_voices(locale)]
