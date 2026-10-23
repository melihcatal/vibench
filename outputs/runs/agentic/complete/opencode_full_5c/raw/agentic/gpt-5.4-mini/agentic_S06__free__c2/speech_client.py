import os
from typing import Optional

from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    AudioOutputConfig,
    SpeechSynthesisOutputFormat,
)

from speech_models import normalize_locale


def load_speech_key() -> Optional[str]:
    return os.getenv("AZURE_SPEECH_KEY")


def load_speech_region() -> Optional[str]:
    return os.getenv("AZURE_SPEECH_REGION")


def build_speech_config() -> SpeechConfig:
    key = load_speech_key()
    region = load_speech_region()
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return SpeechConfig(subscription=key, region=region)


def build_synthesizer(
    output_format: Optional[SpeechSynthesisOutputFormat] = None,
) -> SpeechSynthesizer:
    config = build_speech_config()
    if output_format is not None:
        config.set_speech_synthesis_output_format(output_format)
    return SpeechSynthesizer(
        speech_config=config, audio_config=AudioOutputConfig(use_default_speaker=False)
    )


def target_locale(locale: Optional[str]) -> Optional[str]:
    return normalize_locale(locale)
