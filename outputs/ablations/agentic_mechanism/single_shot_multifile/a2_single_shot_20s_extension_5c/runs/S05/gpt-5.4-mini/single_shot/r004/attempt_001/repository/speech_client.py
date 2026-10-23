import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from deepgram import DeepgramClient


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    model: str = "nova-2"
    language: str = "en-US"
    punctuate: bool = True
    endpointing: int = 500
    sample_rate: int = 16000
    chunk_size: int = 1024


@lru_cache(maxsize=1)
def load_speech_config() -> SpeechConfig:
    api_key = os.getenv("DEEPGRAM_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("DEEPGRAM_API_KEY is required")
    model = os.getenv("DEEPGRAM_MODEL", "nova-2")
    language = os.getenv("DEEPGRAM_LANGUAGE", "en-US")
    punctuate = os.getenv("DEEPGRAM_PUNCTUATE", "true").lower() in {"1", "true", "yes", "on"}
    endpointing = int(os.getenv("DEEPGRAM_ENDPOINTING", "500"))
    sample_rate = int(os.getenv("DEEPGRAM_SAMPLE_RATE", "16000"))
    chunk_size = int(os.getenv("DEEPGRAM_CHUNK_SIZE", "1024"))
    return SpeechConfig(
        api_key=api_key,
        model=model,
        language=language,
        punctuate=punctuate,
        endpointing=endpointing,
        sample_rate=sample_rate,
        chunk_size=chunk_size,
    )


def build_deepgram_client() -> DeepgramClient:
    config = load_speech_config()
    return DeepgramClient(config.api_key)

