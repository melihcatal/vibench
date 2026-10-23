from __future__ import annotations

import os
from functools import lru_cache
from typing import Iterable, List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import VoiceInfo


@lru_cache(maxsize=1)
def get_speech_config() -> speechsdk.SpeechConfig:
    key = os.environ["AZURE_SPEECH_KEY"]
    region = os.environ["AZURE_SPEECH_REGION"]
    config = speechsdk.SpeechConfig(subscription=key, region=region)
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    return config


@lru_cache(maxsize=1)
def get_voice_client() -> speechsdk.SpeechSynthesizer:
    return speechsdk.SpeechSynthesizer(speech_config=get_speech_config(), audio_config=None)


def build_audio_config(output_path: Optional[str] = None):
    if output_path:
        return speechsdk.audio.AudioOutputConfig(filename=output_path)
    return speechsdk.audio.AudioOutputConfig(use_default_speaker=False)


def list_voices(locale_prefix: Optional[str] = None) -> List[VoiceInfo]:
    result = speechsdk.SpeechSynthesizer(speech_config=get_speech_config(), audio_config=None).get_voices_async().get()
    voices = []
    for voice in result.voices:
        info = VoiceInfo(
            name=voice.short_name,
            locale=voice.locale,
            gender=getattr(voice, "gender", None),
            sample_rate_hertz=getattr(voice, "sample_rate_hertz", None),
            natural_sample_rate_hertz=getattr(voice, "voice_type", None),
            extra={"display_name": getattr(voice, "display_name", None), "local_name": getattr(voice, "local_name", None)},
        )
        if locale_prefix is None or info.locale.lower().startswith(locale_prefix.lower()):
            voices.append(info)
    return voices
