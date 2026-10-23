import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str | None = None
    region: str | None = None
    locale: str = "en-US"
    voice: str | None = None


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
        locale=os.getenv("AZURE_SPEECH_LOCALE", "en-US"),
        voice=os.getenv("AZURE_SPEECH_VOICE"),
    )


def ensure_azure_config(config: SpeechConfig | None = None) -> SpeechConfig:
    config = config or load_speech_config()
    if not config.api_key or not config.region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return config
