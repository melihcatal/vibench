from __future__ import annotations

import os
from typing import Any, Dict, Optional

from deepgram import DeepgramClient, DeepgramClientOptions

from speech_models import StreamingRecognitionConfig


DEFAULT_DEEPGRAM_MODEL = "nova-2"
DEFAULT_DEEPGRAM_ENCODING = "linear16"


def load_streaming_config(**overrides: Any) -> StreamingRecognitionConfig:
    config = StreamingRecognitionConfig(
        language=os.getenv("DEEPGRAM_LANGUAGE", "en-US"),
        interim_results=_env_bool("DEEPGRAM_INTERIM_RESULTS", True),
        punctuate=_env_bool("DEEPGRAM_PUNCTUATE", True),
        sample_rate_hz=int(os.getenv("DEEPGRAM_SAMPLE_RATE", "16000")),
        encoding=os.getenv("DEEPGRAM_ENCODING", DEFAULT_DEEPGRAM_ENCODING),
        model=os.getenv("DEEPGRAM_MODEL", DEFAULT_DEEPGRAM_MODEL),
    )
    for key, value in overrides.items():
        if hasattr(config, key) and value is not None:
            setattr(config, key, value)
    return config


def create_deepgram_client(api_key: Optional[str] = None) -> DeepgramClient:
    key = api_key or os.getenv("DEEPGRAM_API_KEY")
    if not key:
        raise ValueError("Missing DEEPGRAM_API_KEY for Deepgram Streaming API")
    options = DeepgramClientOptions(options={"keepalive": "true"})
    return DeepgramClient(key, config=options)


def build_live_options(config: StreamingRecognitionConfig) -> Dict[str, Any]:
    return {
        "model": config.model,
        "language": config.language,
        "encoding": config.encoding,
        "sample_rate": config.sample_rate_hz,
        "interim_results": config.interim_results,
        "punctuate": config.punctuate,
        "smart_format": True,
    }


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
