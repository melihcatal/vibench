from __future__ import annotations

from typing import Any, Callable

from deepgram import LiveTranscriptionEvents

from speech_client import (
    build_live_options,
    create_listen_connection,
    get_deepgram_client,
)
from speech_models import StreamingOptions, normalize_deepgram_result


async def start_streaming_recognizer(
    language_code: str = "en-US",
    punctuate: bool = True,
    on_result: Callable[[Any], Any] | None = None,
):
    client = get_deepgram_client()
    connection = create_listen_connection(client)
    options = build_live_options(
        StreamingOptions(
            language_code=language_code, punctuate=punctuate, interim_results=True
        )
    )

    if on_result is not None:

        async def _handle_transcript(_: Any, result: Any, **__: Any) -> None:
            await on_result(normalize_deepgram_result(result))

        connection.on(LiveTranscriptionEvents.Transcript, _handle_transcript)

    started = await connection.start(options)
    if not started:
        raise RuntimeError("Failed to start Deepgram streaming recognizer")
    return connection
