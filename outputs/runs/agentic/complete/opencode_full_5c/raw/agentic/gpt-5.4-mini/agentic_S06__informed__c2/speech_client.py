import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str
    region: str
    endpoint: str | None = None


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("AZURE_SPEECH_KEY", ""),
        region=os.getenv("AZURE_SPEECH_REGION", ""),
        endpoint=os.getenv("AZURE_SPEECH_ENDPOINT"),
    )


def normalize_locale(locale: str | None) -> str:
    return (locale or "en-US").replace("_", "-")


def create_speech_sdk():
    import azure.cognitiveservices.speech as speechsdk

    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    if cfg.endpoint:
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_Endpoint, cfg.endpoint
        )
    return speechsdk, speech_config
