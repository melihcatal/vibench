import os
from dataclasses import dataclass

from azure.cognitiveservices.speech import SpeechConfig


@dataclass
class SpeechClientConfig:
    key: str
    region: str


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION", ""),
    )


def create_speech_config() -> SpeechConfig:
    cfg = load_speech_config()
    return SpeechConfig(subscription=cfg.key, region=cfg.region)
