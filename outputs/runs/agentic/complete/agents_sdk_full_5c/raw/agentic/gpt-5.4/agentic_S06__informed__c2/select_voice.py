from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import DEFAULT_TTS_LANGUAGE, DEFAULT_TTS_VOICE, GoogleTTSClientFactory
from speech_models import VoiceOption


PROVIDER = "google-cloud-texttospeech"


def list_voices(locale: Optional[str] = None) -> List[VoiceOption]:
    client = GoogleTTSClientFactory.create_client()
    language_code = locale or DEFAULT_TTS_LANGUAGE
    response = client.list_voices(language_code=language_code)
    return [
        VoiceOption(
            name=voice.name,
            language_codes=list(voice.language_codes),
            gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            natural_sample_rate_hz=voice.natural_sample_rate_hertz,
        )
        for voice in response.voices
    ]


def select_voice(locale: str, preferred_name: Optional[str] = None) -> VoiceOption:
    voices = list_voices(locale)
    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return voice
    for voice in voices:
        if "Neural2" in voice.name:
            return voice
    for voice in voices:
        if voice.name == DEFAULT_TTS_VOICE:
            return voice
    if not voices:
        raise LookupError(f"No Google Cloud Text-to-Speech voices available for {locale}")
    return voices[0]
