import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str
    region: str
    language_code: str = "en-US"
    punctuate: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION", ""),
        language_code=os.environ.get("SPEECH_LANGUAGE", "en-US"),
        punctuate=os.environ.get("SPEECH_PUNCTUATE", "1") != "0",
    )


def speech_headers() -> dict:
    cfg = load_speech_config()
    return {"Ocp-Apim-Subscription-Key": cfg.api_key, "X-Region": cfg.region}
