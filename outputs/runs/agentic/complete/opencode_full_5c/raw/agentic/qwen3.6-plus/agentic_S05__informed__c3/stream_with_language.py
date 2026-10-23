from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator

from deepgram import DeepgramClient, LiveTranscriptionEvents

from speech_client import create_deepgram_client
from speech_models import TranscriptResult, normalize_deepgram_result, StreamingEvent

logger = logging.getLogger(__name__)


async def stream_with_language(
    language: str,
    audio_source: AsyncGenerator[bytes, None],
    punctuate: bool = True,
    model: str | None = None,
    profanity_filter: bool = False,
    diarize: bool = False,
    client: DeepgramClient | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    if client is None:
        client = create_deepgram_client()

    options = {
        "model": model or "nova-2",
        "language": language,
        "punctuate": punctuate,
        "interim_results": True,
        "smart_format": True,
        "profanity_filter": profanity_filter,
        "diarize": diarize,
    }

    queue: asyncio.Queue[StreamingEvent | None] = asyncio.Queue()

    async def on_transcript(data):
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
                LiveTranscriptionEvents.Transcript: on_transcript,
            },
        )

        logger.info(
            "Deepgram streaming started: language=%s, punctuate=%s, model=%s",
            language,
            punctuate,
            options.get("model"),
        )

        try:
            async for pcm_bytes in audio_source:
                await dg_connection.send(pcm_bytes)

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
        logger.error("Deepgram streaming with language error: %s", exc)
        raise
