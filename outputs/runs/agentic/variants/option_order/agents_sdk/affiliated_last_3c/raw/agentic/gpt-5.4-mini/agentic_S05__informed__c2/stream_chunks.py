from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import build_deepgram_client, build_live_options, load_stream_config, transcript_chunk_from_event


async def stream_chunks(audio_chunks: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = build_deepgram_client()
    config = load_stream_config()
    options = build_live_options(config)
    conn = await client.listen.asyncwebsocket.v("1")
    await conn.start(options)
    async for chunk in audio_chunks:
        await conn.send(chunk)
        event = await conn.receive()
        transcript = transcript_chunk_from_event(event)
        if transcript.text:
            yield transcript.text
    await conn.finish()
