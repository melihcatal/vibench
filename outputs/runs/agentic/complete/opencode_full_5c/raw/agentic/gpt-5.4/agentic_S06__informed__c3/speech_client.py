from __future__ import annotations

import os
from functools import lru_cache

import azure.cognitiveservices.speech as speechsdk


AZURE_TTS_PROVIDER = "azure-ai-speech"
DEFAULT_TTS_FORMAT = "audio-24khz-48kbitrate-mono-mp3"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_speech_config() -> speechsdk.SpeechConfig:
    speech_config = speechsdk.SpeechConfig(
        subscription=require_env("AZURE_SPEECH_KEY"),
        region=require_env("AZURE_SPEECH_REGION"),
    )
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3
    )
    return speech_config


def build_synthesizer(
    audio_config: speechsdk.audio.AudioOutputConfig | None = None,
) -> speechsdk.SpeechSynthesizer:
    return speechsdk.SpeechSynthesizer(
        speech_config=get_speech_config(), audio_config=audio_config
    )


def output_format_name() -> str:
    return DEFAULT_TTS_FORMAT
