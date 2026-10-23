from __future__ import annotations

import asyncio
from typing import AsyncIterator

from speech_client import SpeechConfig, build_live_options, create_deepgram_client
from speech_models import StreamingTranscript, normalize_transcript


async def stream_microphone() -> AsyncIterator[StreamingTranscript]:
    config = SpeechConfig.from_env()
    client = create_deepgram_client(config)
    connection = await client.listen.asyncwebsocket.v("1")
    options = build_live_options(config)

    async def _on_message(message):
        transcript = normalize_transcript(message)
        if transcript.text:
            queue.put_nowait(transcript)

    queue: asyncio.Queue[StreamingTranscript] = asyncio.Queue()
    connection.on("Transcript", _on_message)
    await connection.start(options)

    try:
        while True:
            yield await queue.get()
    finally:
        await connection.finish()
