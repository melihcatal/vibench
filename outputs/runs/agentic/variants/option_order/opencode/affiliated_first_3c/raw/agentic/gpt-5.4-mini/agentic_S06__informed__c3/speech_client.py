import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    region: str
    voice_name: Optional[str] = None
    language: Optional[str] = None
    output_format: Optional[str] = None


@lru_cache(maxsize=1)
def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION", ""),
        voice_name=os.environ.get("AZURE_SPEECH_VOICE"),
        language=os.environ.get("AZURE_SPEECH_LANGUAGE"),
        output_format=os.environ.get("AZURE_SPEECH_OUTPUT_FORMAT"),
    )


def require_config() -> SpeechConfig:
    config = load_speech_config()
    if not config.api_key or not config.region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return config
