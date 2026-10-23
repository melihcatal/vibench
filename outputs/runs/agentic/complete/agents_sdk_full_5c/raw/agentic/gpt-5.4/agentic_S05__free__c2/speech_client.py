from __future__ import annotations

import os
from typing import Optional

from deepgram import AsyncDeepgramClient, DeepgramClient

from speech_models import StreamingConfig


DEEPGRAM_API_KEY_ENV = "DEEPGRAM_API_KEY"
DEEPGRAM_LIVE_PATH = "wss://api.deepgram.com/v1/listen"
DEEPGRAM_MODEL = "nova-2"


def get_api_key(explicit: Optional[str] = None) -> str:
    api_key = explicit or os.getenv(DEEPGRAM_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing {DEEPGRAM_API_KEY_ENV} for Deepgram API access")
    return api_key


def build_streaming_options(config: Optional[StreamingConfig] = None) -> dict:
    cfg = config or StreamingConfig()
    return {
        "model": cfg.model or DEEPGRAM_MODEL,
        "language": cfg.language_code,
        "encoding": cfg.encoding,
        "sample_rate": cfg.sample_rate_hz,
        "interim_results": cfg.interim_results,
        "smart_format": cfg.punctuate,
        "profanity_filter": cfg.profanity_filter,
        "endpointing": 300,
        "vad_events": True,
    }


def create_client(api_key: Optional[str] = None) -> DeepgramClient:
    return DeepgramClient(get_api_key(api_key))


def create_async_client(api_key: Optional[str] = None) -> AsyncDeepgramClient:
    return AsyncDeepgramClient(get_api_key(api_key))
