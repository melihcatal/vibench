from __future__ import annotations

from collections.abc import AsyncIterable
from collections.abc import AsyncIterator

from deepgram import LiveTranscriptionEvents

from partial_results import PartialResultsHandler
from speech_client import open_live_connection
from speech_models import StreamingConfig
from speech_models import TranscriptEvent


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes],
    *,
    config: StreamingConfig | None = None,
) -> AsyncIterator[TranscriptEvent]:
    connection = await open_live_connection(config)
    handler = PartialResultsHandler()
    queue: list[TranscriptEvent] = []

    async def on_message(_: object, result: object, **__: object) -> None:
        event = handler.handle(result)
        if event.text:
            queue.append(event)

    connection.on(LiveTranscriptionEvents.Transcript, on_message)

    async for chunk in audio_source:
        if chunk:
            await connection.send(chunk)
        while queue:
            yield queue.pop(0)

    await connection.finish()
    while queue:
        yield queue.pop(0)
