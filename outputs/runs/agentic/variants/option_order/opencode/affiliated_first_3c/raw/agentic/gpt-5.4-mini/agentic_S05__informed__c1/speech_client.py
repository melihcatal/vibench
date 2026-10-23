import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str
    region: str | None = None
    language: str = "en-US"
    enable_punctuation: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION"),
        language=os.environ.get("SPEECH_LANGUAGE", "en-US"),
        enable_punctuation=os.environ.get("SPEECH_ENABLE_PUNCTUATION", "1") != "0",
    )


def make_azure_speech_config(speechsdk):
    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    if cfg.enable_punctuation:
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
            "TrueText",
        )
    return speech_config


def iter_audio_frames(source):
    if hasattr(source, "__aiter__"):
        return source
    return source
