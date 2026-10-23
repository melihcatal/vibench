from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncGenerator

from speech_client import DeepgramSpeechClient
from speech_models import StreamingUtterance


async def stream_chunks(chunks: AsyncIterable[bytes]) -> AsyncGenerator[StreamingUtterance, None]:
    from deepgram import LiveTranscriptionEvents  # provider-identifying import

    client = DeepgramSpeechClient()
    live = client.client().listen.websocket.v("1")
    options = client.live_options()
    queue: list[StreamingUtterance] = []

    def on_message(_, result, **__):
        utterance = client.transcribe_event(result)
        if utterance.text:
            queue.append(utterance)

    live.on(LiveTranscriptionEvents.Transcript, on_message)
    live.start(options)
    try:
        async for chunk in chunks:
            if chunk:
                live.send(chunk)
                await asyncio.sleep(0)
            while queue:
                yield queue.pop(0)
    finally:
        live.finish()
