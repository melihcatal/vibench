from typing import List

from speech_client import preferred_voice
from speech_models import VoiceOption, normalize_locale


AZURE_VOICES: List[VoiceOption] = [
    VoiceOption(name="en-US-AriaNeural", locale="en-US", gender="Female", short_name="AriaNeural"),
    VoiceOption(name="en-US-GuyNeural", locale="en-US", gender="Male", short_name="GuyNeural"),
    VoiceOption(name="en-GB-LibbyNeural", locale="en-GB", gender="Female", short_name="LibbyNeural"),
    VoiceOption(name="es-ES-ElviraNeural", locale="es-ES", gender="Female", short_name="ElviraNeural"),
]


def list_voices(locale: str = None) -> List[VoiceOption]:
    locale = normalize_locale(locale or "")
    if not locale:
        return AZURE_VOICES
    return [voice for voice in AZURE_VOICES if normalize_locale(voice.locale) == locale]


def select_voice(locale: str = "en-US") -> str:
    voices = list_voices(locale)
    if voices:
        return voices[0].short_name or voices[0].name
    return preferred_voice(locale)
