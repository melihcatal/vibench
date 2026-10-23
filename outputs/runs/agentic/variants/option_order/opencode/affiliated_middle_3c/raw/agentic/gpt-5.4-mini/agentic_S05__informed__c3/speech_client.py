import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SpeechConfig:
    deepgram_api_key: str
    model: str = "nova-2"
    language: Optional[str] = None
    smart_format: bool = True


def load_config() -> SpeechConfig:
    return SpeechConfig(
        deepgram_api_key=os.environ.get("DEEPGRAM_API_KEY", ""),
        model=os.environ.get("DEEPGRAM_MODEL", "nova-2"),
        language=os.environ.get("DEEPGRAM_LANGUAGE"),
        smart_format=os.environ.get("DEEPGRAM_SMART_FORMAT", "1") != "0",
    )


def build_deepgram_options(config: Optional[SpeechConfig] = None) -> dict:
    config = config or load_config()
    return {
        "model": config.model,
        "language": config.language,
        "punctuate": config.smart_format,
        "smart_format": config.smart_format,
        "interim_results": True,
    }
