from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional

from speech_client import open_stream
from speech_models import StreamingConfig


async def start_streaming_recognizer(
    language_code: str,
    punctuate: bool,
    on_transcript: Callable[[Any], Awaitable[None]],
    sample_rate_hz: int = 16000,
) -> Any:
    config = StreamingConfig(
        sample_rate_hz=sample_rate_hz,
        language_code=language_code,
        interim_results=True,
        punctuate=punctuate,
    )
    return await open_stream(config, on_transcript)
