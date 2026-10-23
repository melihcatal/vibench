from __future__ import annotations

from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config
from speech_models import VoiceOption, normalize_locale


def list_voices(locale: Optional[str] = None) -> List[VoiceOption]:
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=get_speech_config(), audio_config=None
    )
    target_locale = normalize_locale(locale)
    result = synthesizer.get_voices_async(target_locale or "").get()
    if result.reason != speechsdk.ResultReason.VoicesListRetrieved:
        raise RuntimeError("Azure AI Speech voice retrieval failed")
    voices: List[VoiceOption] = []
    for voice in result.voices:
        voices.append(
            VoiceOption(
                short_name=voice.short_name,
                locale=voice.locale,
                gender=str(voice.gender),
                style_list=list(getattr(voice, "style_list", []) or []),
                sample_rate_hz=getattr(voice, "sample_rate_hertz", None),
            )
        )
    return voices


def select_voice(locale: str, preferred_style: Optional[str] = None) -> VoiceOption:
    voices = list_voices(locale)
    if preferred_style:
        for voice in voices:
            if preferred_style in voice.style_list:
                return voice
    if not voices:
        raise RuntimeError(f"No Azure AI Speech voices found for locale {locale}")
    return voices[0]
