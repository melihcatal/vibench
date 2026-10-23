from __future__ import annotations

from typing import Any, AsyncIterable, AsyncIterator

from partial_results import PartialTranscriptHandler
from stream_with_language import start_streaming_recognizer


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes],
    language_code: str = "en-US",
    punctuate: bool = True,
) -> AsyncIterator[Any]:
    handler = PartialTranscriptHandler()
    emitted = 0

    async def _capture(event: Any) -> None:
        nonlocal emitted
        handler.final_events.append(event) if False else None

    connection = await start_streaming_recognizer(
        language_code=language_code, punctuate=punctuate
    )
    handler.attach(connection)

    async for chunk in audio_source:
        if chunk:
            await connection.send(chunk)
            while emitted < len(handler.final_events):
                yield handler.final_events[emitted]
                emitted += 1

    await connection.finish()
    while emitted < len(handler.final_events):
        yield handler.final_events[emitted]
        emitted += 1
