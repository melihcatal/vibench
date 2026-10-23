import os
from dataclasses import dataclass
from typing import Optional


def env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value not in ("", None) else default


@dataclass
class SpeechServiceConfig:
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    model: Optional[str] = None


def load_speech_config() -> SpeechServiceConfig:
    return SpeechServiceConfig(
        api_key=env("ASSEMBLYAI_API_KEY"),
        api_url=env("ASSEMBLYAI_API_URL", "https://api.assemblyai.com"),
        model=env("ASSEMBLYAI_MODEL", "best"),
    )
