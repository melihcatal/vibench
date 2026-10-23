import os
from dataclasses import dataclass
from typing import Optional

from deepgram import DeepgramClient


@dataclass
class SpeechConfig:
    api_key: str
    language: Optional[str] = None
    punctuate: bool = True
    interim_results: bool = True
    model: str = "nova-2"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        language=os.getenv("DEEPGRAM_LANGUAGE"),
        punctuate=os.getenv("DEEPGRAM_PUNCTUATE", "true").lower() == "true",
        interim_results=os.getenv("DEEPGRAM_INTERIM_RESULTS", "true").lower() == "true",
        model=os.getenv("DEEPGRAM_MODEL", "nova-2"),
    )


def create_client(config: Optional[SpeechConfig] = None) -> DeepgramClient:
    config = config or load_speech_config()
    return DeepgramClient(config.api_key)


def base_options(config: Optional[SpeechConfig] = None) -> dict:
    config = config or load_speech_config()
    options = {
        "model": config.model,
        "punctuate": config.punctuate,
        "interim_results": config.interim_results,
    }
    if config.language:
        options["language"] = config.language
    return options
