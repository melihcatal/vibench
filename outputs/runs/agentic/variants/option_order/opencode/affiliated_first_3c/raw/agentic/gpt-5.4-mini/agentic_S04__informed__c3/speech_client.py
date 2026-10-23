import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str
    region: str
    language: str


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION", ""),
        language=os.environ.get("SPEECH_LANGUAGE", "en-US"),
    )


def build_azure_speech_client() -> object:
    import azure.cognitiveservices.speech as speechsdk

    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language
    return speechsdk, speech_config
