from __future__ import annotations

import os
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk


def _speech_config() -> speechsdk.SpeechConfig:
    key = os.getenv("AZURE_SPEECH_KEY", "")
    region = os.getenv("AZURE_SPEECH_REGION", "")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return speechsdk.SpeechConfig(subscription=key, region=region)


def list_voices(locale: Optional[str] = None) -> List[str]:
    client = speechsdk.SpeechSynthesizer(speech_config=_speech_config(), audio_config=None)
    result = client.get_voices_async(locale or "").get()
    if not result.voices:
        return []
    return [voice.short_name for voice in result.voices]


def select_voice(locale: str, preferred_voice: Optional[str] = None) -> str:
    voices = list_voices(locale)
    if preferred_voice and preferred_voice in voices:
        return preferred_voice
    if voices:
        return voices[0]
    raise RuntimeError(f"No Azure voice found for locale={locale}")
