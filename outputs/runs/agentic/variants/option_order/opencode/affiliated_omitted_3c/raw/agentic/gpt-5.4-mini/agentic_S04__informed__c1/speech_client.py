import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SpeechConfig:
    api_key: str
    base_url: Optional[str] = None
    model: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("ASSEMBLYAI_API_KEY", ""),
        base_url=os.environ.get("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com"),
        model=os.environ.get("ASSEMBLYAI_MODEL", "best"),
    )
