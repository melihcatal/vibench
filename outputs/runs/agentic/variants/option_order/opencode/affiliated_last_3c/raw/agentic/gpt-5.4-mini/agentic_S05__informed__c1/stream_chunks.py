from typing import Any, AsyncIterator

from speech_client import build_live_options, create_deepgram_client, iter_bytes
from speech_models import TranscriptChunk, normalize_transcript


async def stream_chunks(source: Any) -> AsyncIterator[TranscriptChunk]:
    client = create_deepgram_client()
    connection = await client.listen.asyncwebsocket.v("1")
    await connection.start(build_live_options())
    async for chunk in iter_bytes(source):
        await connection.send(chunk)
        event = await connection.receive()
        transcript = normalize_transcript(event)
        if transcript.text:
            yield transcript
    await connection.finish()
