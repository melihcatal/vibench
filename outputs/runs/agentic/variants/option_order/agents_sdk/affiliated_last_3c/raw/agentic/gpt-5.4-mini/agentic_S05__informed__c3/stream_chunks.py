from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

from speech_client import DeepgramSpeechClient
from speech_models import TranscriptChunk, TranscriptEvent


async def stream_chunks(chunks: AsyncIterable[TranscriptChunk]) -> AsyncIterator[TranscriptEvent]:
    client = DeepgramSpeechClient()
    dg = client.client
    conn = dg.listen.websocket.v("1")
    options = LiveOptions(**client._options())
    queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()

    def on_message(_, result, **__):
        queue.put_nowait(client.process_event(result.to_dict()))

    conn.on(LiveTranscriptionEvents.Transcript, on_message)
    conn.start(options)
    async for chunk in chunks:
        conn.send(chunk.audio)
        while not queue.empty():
            yield await queue.get()
    conn.finish()
