from __future__ import annotations

from typing import AsyncIterator, Iterable

from speech_client import SpeechConfig, build_live_options, create_deepgram_client
from speech_models import StreamingChunk, StreamingTranscript, normalize_transcript


async def stream_chunks(source: AsyncIterator[bytes] | Iterable[bytes]) -> AsyncIterator[StreamingTranscript]:
    config = SpeechConfig.from_env()
    client = create_deepgram_client(config)
    connection = await client.listen.asyncwebsocket.v("1")
    await connection.start(build_live_options(config))

    async def _aiter():
        if hasattr(source, "__aiter__"):
            async for chunk in source:
                yield chunk
        else:
            for chunk in source:
                yield chunk

    try:
        async for payload in _aiter():
            if isinstance(payload, StreamingChunk):
                await connection.send(payload.audio)
            else:
                await connection.send(payload)
            event = await connection.recv()
            transcript = normalize_transcript(event)
            if transcript.text:
                yield transcript
    finally:
        await connection.finish()
