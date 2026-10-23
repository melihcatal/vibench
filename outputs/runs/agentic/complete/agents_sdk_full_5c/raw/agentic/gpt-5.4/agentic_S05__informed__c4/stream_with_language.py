from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator

from deepgram.clients.listen.v1.websocket.client import AsyncListenWebSocketClient
from deepgram.clients.listen.v1.websocket.enums import LiveTranscriptionEvents

from speech_client import build_live_options, get_deepgram_client, send_audio_chunks
from speech_models import TranscriptSegment, normalize_transcript_text


async def start_streaming_recognizer(
    audio_source: AsyncIterable[bytes],
    *,
    language: str = "en-US",
    punctuate: bool = True,
) -> AsyncIterator[TranscriptSegment]:
    client = get_deepgram_client()
    connection: AsyncListenWebSocketClient = client.listen.asyncwebsocket.v("1")
    queue: asyncio.Queue[TranscriptSegment | None] = asyncio.Queue()

    async def on_transcript(_client, result, **_kwargs):
        alt = result.channel.alternatives[0]
        text = normalize_transcript_text(alt.transcript)
        if text:
            await queue.put(
                TranscriptSegment(
                    text=text,
                    is_final=bool(getattr(result, "is_final", False)),
                    confidence=getattr(alt, "confidence", None),
                    language_code=language,
                    raw=result,
                )
            )

    async def on_close(*_args, **_kwargs):
        await queue.put(None)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.on(LiveTranscriptionEvents.Close, on_close)
    await connection.start(
        build_live_options(language=language, punctuate=punctuate, interim_results=True)
    )

    sender = asyncio.create_task(send_audio_chunks(connection, audio_source))
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        await sender
