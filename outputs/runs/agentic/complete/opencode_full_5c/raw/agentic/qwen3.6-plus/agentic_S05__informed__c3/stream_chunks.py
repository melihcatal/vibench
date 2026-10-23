from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator

from deepgram import DeepgramClient, LiveTranscriptionEvents

from speech_client import create_deepgram_client, build_streaming_options
from speech_models import (
    AudioChunk,
    TranscriptResult,
    normalize_deepgram_result,
    StreamingEvent,
)

logger = logging.getLogger(__name__)


async def stream_chunks(
    audio_source: AsyncGenerator[AudioChunk, None],
    language: str | None = None,
    model: str | None = None,
    client: DeepgramClient | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    if client is None:
        client = create_deepgram_client()

    options = build_streaming_options(
        language=language,
        model=model,
        punctuate=True,
        interim_results=True,
    )

    queue: asyncio.Queue[StreamingEvent | None] = asyncio.Queue()

    async def on_transcript_received(data):
        try:
            payload = data.__dict__ if hasattr(data, "__dict__") else {}
            if "is_final" in payload or "channel" in payload:
                result = normalize_deepgram_result(payload)
                event = StreamingEvent(
                    event_type="final" if result.is_final else "interim",
                    result=result,
                    raw_payload=payload,
                )
                await queue.put(event)
        except Exception as exc:
            logger.error("Error processing transcript: %s", exc)

    try:
        dg_connection = client.listen.asyncwebsocket.v("1")

        await dg_connection.start(
            options=options,
            event_handler={
                LiveTranscriptionEvents.Transcript: on_transcript_received,
            },
        )

        logger.info(
            "Streaming audio chunks with Deepgram model %s", options.get("model")
        )

        try:
            async for chunk in audio_source:
                await dg_connection.send(chunk.pcm_bytes)

                while not queue.empty():
                    item = await queue.get()
                    if item is None:
                        return
                    yield item

                await asyncio.sleep(0.01)

            await dg_connection.finalize()

            while not queue.empty():
                item = await queue.get()
                if item is None:
                    return
                yield item
        except asyncio.CancelledError:
            raise
        finally:
            await dg_connection.finish()
    except Exception as exc:
        logger.error("Deepgram chunk streaming error: %s", exc)
        raise
