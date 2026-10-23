import os
from typing import List, Optional

from openai import OpenAI

from speech_models import VoiceChoice, normalize_locale


def _api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


def client() -> OpenAI:
    return OpenAI(api_key=_api_key())


def default_tts_model() -> str:
    return os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def default_transcribe_model() -> str:
    return os.getenv("OPENAI_TRANSCRIBE_MODEL", "whisper-1")


def default_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def select_matching_voice(voices: List[VoiceChoice], target_locale: Optional[str]) -> Optional[VoiceChoice]:
    if not voices:
        return None
    locale = normalize_locale(target_locale)
    if locale is None:
        return voices[0]
    for voice in voices:
        if normalize_locale(voice.locale) == locale:
            return voice
    return voices[0]
