import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_PROVIDER = "assemblyai"
DEFAULT_MODEL = "assemblyai-universal"

@dataclass
class SpeechConfig:
    api_key: Optional[str]
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL


def load_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("ASSEMBLYAI_API_KEY"),
        provider=os.getenv("SPEECH_PROVIDER", DEFAULT_PROVIDER),
        model=os.getenv("SPEECH_MODEL", DEFAULT_MODEL),
    )


def require_api_key() -> str:
    cfg = load_config()
    if not cfg.api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return cfg.api_key
