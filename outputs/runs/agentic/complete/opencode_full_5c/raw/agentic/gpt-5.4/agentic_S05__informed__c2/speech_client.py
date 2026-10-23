from __future__ import annotations

import os
from typing import Any

from deepgram import DeepgramClient, LiveOptions

from speech_models import StreamingOptions


def get_deepgram_client(api_key: str | None = None) -> DeepgramClient:
    resolved_key = api_key or os.getenv("DEEPGRAM_API_KEY")
    if not resolved_key:
        raise ValueError("DEEPGRAM_API_KEY is required")
    return DeepgramClient(resolved_key)


def build_live_options(options: StreamingOptions | None = None) -> LiveOptions:
    config = options or StreamingOptions()
    return LiveOptions(
        model=config.model,
        language=config.language_code,
        interim_results=config.interim_results,
        punctuate=config.punctuate,
        smart_format=True,
        channels=config.channels,
        sample_rate=config.sample_rate_hz,
        encoding=config.encoding,
    )


def create_listen_connection(client: DeepgramClient) -> Any:
    return client.listen.asynclive.v("1")
