import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str
    region: str
    model: str = "transcription"


def load_speech_config(config=None):
    config = config or {}
    return SpeechConfig(
        api_key=config.get("api_key") or os.environ["AZURE_SPEECH_KEY"],
        region=config.get("region") or os.environ["AZURE_SPEECH_REGION"],
        model=config.get("model") or "transcription",
    )


def speech_headers(api_key):
    return {"Ocp-Apim-Subscription-Key": api_key}
