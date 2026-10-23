import os
from dataclasses import dataclass

import azure.cognitiveservices.speech as speechsdk


@dataclass
class SpeechSettings:
    api_key: str
    region: str
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    enable_punctuation: bool = True


def load_settings(config=None, payload=None):
    config = config or {}
    payload = payload or {}
    return SpeechSettings(
        api_key=config.get("api_key") or os.environ["AZURE_SPEECH_KEY"],
        region=config.get("region") or os.environ["AZURE_SPEECH_REGION"],
        language_code=payload.get("language_code", config.get("language_code", "en-US")),
        sample_rate_hz=payload.get("sample_rate_hz", config.get("sample_rate_hz", 16000)),
        enable_punctuation=payload.get("enable_punctuation", config.get("enable_punctuation", True)),
    )


def build_speech_config(settings):
    speech_config = speechsdk.SpeechConfig(subscription=settings.api_key, region=settings.region)
    speech_config.speech_recognition_language = settings.language_code
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
                              "TrueText" if settings.enable_punctuation else "Lexical")
    return speech_config


def audio_format(settings):
    return speechsdk.audio.AudioStreamFormat(samples_per_second=settings.sample_rate_hz, bits_per_sample=16, channels=1)
