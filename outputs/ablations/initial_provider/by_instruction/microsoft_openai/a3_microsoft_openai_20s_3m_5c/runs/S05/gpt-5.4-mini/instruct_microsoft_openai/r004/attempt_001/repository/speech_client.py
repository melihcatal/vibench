import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SpeechConfig:
    microsoft_speech_key: Optional[str]
    microsoft_speech_region: Optional[str]
    openai_api_key: Optional[str]


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        microsoft_speech_key=os.getenv("AZURE_SPEECH_KEY"),
        microsoft_speech_region=os.getenv("AZURE_SPEECH_REGION"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )


def require_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def require_azure_speech_config() -> tuple[str, str]:
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return key, region
