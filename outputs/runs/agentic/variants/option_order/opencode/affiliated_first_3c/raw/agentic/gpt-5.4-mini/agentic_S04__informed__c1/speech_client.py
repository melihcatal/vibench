import os
from dataclasses import dataclass


@dataclass
class SpeechClientConfig:
    api_key: str
    region: str | None = None


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION"),
    )


def require_speech_config() -> SpeechClientConfig:
    config = load_speech_config()
    if not config.api_key or not config.region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return config


def create_speech_sdk_config():
    import azure.cognitiveservices.speech as speechsdk

    config = require_speech_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    return speechsdk, speech_config
