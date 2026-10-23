from __future__ import annotations

import asyncio
from typing import AsyncIterator, Callable, Optional

from deepgram.clients.listen.v1.websocket.client import AsyncListenWebSocketClient
from deepgram.clients.listen.v1.websocket.enums import LiveTranscriptionEvents

from speech_client import build_live_options, get_deepgram_client, send_audio_chunks
from speech_models import TranscriptSegment, normalize_transcript_text


async def stream_microphone_audio(
    microphone_source: AsyncIterator[bytes],
    *,
    on_interim: Optional[Callable[[TranscriptSegment], None]] = None,
) -> AsyncIterator[TranscriptSegment]:
    client = get_deepgram_client()
    connection: AsyncListenWebSocketClient = client.listen.asyncwebsocket.v("1")
    results_queue: asyncio.Queue[Optional[TranscriptSegment]] = asyncio.Queue()

    async def handle_transcript(_client, result, **_kwargs):
        alternative = result.channel.alternatives[0]
        text = normalize_transcript_text(alternative.transcript)
        if not text:
            return
        segment = TranscriptSegment(
            text=text,
            is_final=bool(getattr(result, "is_final", False)),
            confidence=getattr(alternative, "confidence", None),
            raw=result,
        )
        if not segment.is_final and on_interim:
            on_interim(segment)
        await results_queue.put(segment)

    async def handle_close(*_args, **_kwargs):
        await results_queue.put(None)

    connection.on(LiveTranscriptionEvents.Transcript, handle_transcript)
    connection.on(LiveTranscriptionEvents.Close, handle_close)
    await connection.start(build_live_options(interim_results=True, punctuate=True))

    sender = asyncio.create_task(send_audio_chunks(connection, microphone_source))
    try:
        while True:
            item = await results_queue.get()
            if item is None:
                break
            yield item
    finally:
        await sender
