from __future__ import annotations

import os
from typing import Any

from deepgram import AsyncDeepgramClient
from deepgram import DeepgramClientOptions
from deepgram import LiveOptions

from speech_models import StreamingConfig


def load_streaming_config(
    *,
    language: str = "en-US",
    punctuate: bool = True,
    interim_results: bool = True,
) -> StreamingConfig:
    return StreamingConfig(
        sample_rate=int(os.getenv("DEEPGRAM_SAMPLE_RATE", "16000")),
        channels=int(os.getenv("DEEPGRAM_CHANNELS", "1")),
        encoding=os.getenv("DEEPGRAM_ENCODING", "linear16"),
        language=language,
        interim_results=interim_results,
        punctuate=punctuate,
        endpointing_ms=int(os.getenv("DEEPGRAM_ENDPOINTING_MS", "300")),
        utterance_end_ms=int(os.getenv("DEEPGRAM_UTTERANCE_END_MS", "1000")),
        model=os.getenv("DEEPGRAM_MODEL", "nova-2"),
    )


def build_deepgram_client() -> AsyncDeepgramClient:
    api_key = os.environ["DEEPGRAM_API_KEY"]
    options = DeepgramClientOptions(options={"keepalive": "true"})
    return AsyncDeepgramClient(api_key, config=options)


def build_live_options(config: StreamingConfig) -> LiveOptions:
    return LiveOptions(
        model=config.model,
        language=config.language,
        encoding=config.encoding,
        channels=config.channels,
        sample_rate=config.sample_rate,
        interim_results=config.interim_results,
        punctuate=config.punctuate,
        endpointing=config.endpointing_ms,
        utterance_end_ms=str(config.utterance_end_ms),
        smart_format=True,
    )


async def open_live_connection(config: StreamingConfig | None = None) -> Any:
    active_config = config or load_streaming_config()
    client = build_deepgram_client()
    connection = client.listen.asynclive.v("1")
    accepted = await connection.start(build_live_options(active_config))
    if not accepted:
        raise RuntimeError("Deepgram live transcription connection failed to start")
    return connection
