from __future__ import annotations

from typing import Iterable, Optional

from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

from speech_client import SpeechClientFactory


def list_or_select_voice(target_locale: str, preferred_voice: Optional[str] = None) -> str:
    cfg = SpeechClientFactory.from_env()
    speech_config = SpeechConfig(subscription=cfg.key, region=cfg.region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    voices = synthesizer.get_voices_async(target_locale).get().voices
    if preferred_voice:
        for voice in voices:
            if voice.short_name == preferred_voice:
                return voice.short_name
    for voice in voices:
        if getattr(voice, "locale", None) == target_locale:
            return voice.short_name
    return voices[0].short_name if voices else cfg.voice or ""
