from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from deepgram import DeepgramClient, LiveOptions


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    model: str = "nova-2"
    language: Optional[str] = None
    punctuate: bool = True
    interim_results: bool = True
    smart_format: bool = True

    @classmethod
    def from_env(cls) -> "SpeechConfig":
        return cls(
            api_key=os.environ["DEEPGRAM_API_KEY"],
            model=os.getenv("DEEPGRAM_MODEL", "nova-2"),
            language=os.getenv("DEEPGRAM_LANGUAGE") or None,
            punctuate=os.getenv("DEEPGRAM_PUNCTUATE", "true").lower() == "true",
            interim_results=os.getenv("DEEPGRAM_INTERIM_RESULTS", "true").lower() == "true",
            smart_format=os.getenv("DEEPGRAM_SMART_FORMAT", "true").lower() == "true",
        )


def create_deepgram_client(config: Optional[SpeechConfig] = None) -> DeepgramClient:
    cfg = config or SpeechConfig.from_env()
    return DeepgramClient(cfg.api_key)


def build_live_options(config: Optional[SpeechConfig] = None, **overrides) -> LiveOptions:
    cfg = config or SpeechConfig.from_env()
    options = {
        "model": cfg.model,
        "language": cfg.language,
        "punctuate": cfg.punctuate,
        "interim_results": cfg.interim_results,
        "smart_format": cfg.smart_format,
        **overrides,
    }
    return LiveOptions(**{k: v for k, v in options.items() if v is not None})
