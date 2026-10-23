from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator

from deepgram.clients.listen.v1.websocket.client import AsyncListenWebSocketClient
from deepgram.clients.listen.v1.websocket.enums import LiveTranscriptionEvents

from speech_client import build_live_options, get_deepgram_client, send_audio_chunks
from speech_models import StreamingAudioChunk, TranscriptSegment, normalize_transcript_text


async def transcribe_audio_chunks(
    chunks: AsyncIterable[StreamingAudioChunk | bytes],
) -> AsyncIterator[TranscriptSegment]:
    client = get_deepgram_client()
    connection: AsyncListenWebSocketClient = client.listen.asyncwebsocket.v("1")
    output: asyncio.Queue[TranscriptSegment | None] = asyncio.Queue()

    async def on_message(_client, result, **_kwargs):
        alt = result.channel.alternatives[0]
        text = normalize_transcript_text(alt.transcript)
        if text:
            await output.put(
                TranscriptSegment(
                    text=text,
                    is_final=bool(getattr(result, "is_final", False)),
                    confidence=getattr(alt, "confidence", None),
                    raw=result,
                )
            )

    async def on_close(*_args, **_kwargs):
        await output.put(None)

    connection.on(LiveTranscriptionEvents.Transcript, on_message)
    connection.on(LiveTranscriptionEvents.Close, on_close)
    await connection.start(build_live_options())

    producer = asyncio.create_task(send_audio_chunks(connection, chunks))
    try:
        while True:
            item = await output.get()
            if item is None:
                break
            yield item
    finally:
        await producer
