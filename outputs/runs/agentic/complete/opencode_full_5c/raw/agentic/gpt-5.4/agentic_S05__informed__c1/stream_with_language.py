from __future__ import annotations

from typing import Any

from speech_client import load_streaming_config
from speech_client import open_live_connection


async def start_streaming_recognizer(
    *,
    language: str = "en-US",
    punctuate: bool = True,
    interim_results: bool = True,
) -> Any:
    config = load_streaming_config(
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
    )
    return await open_live_connection(config)
