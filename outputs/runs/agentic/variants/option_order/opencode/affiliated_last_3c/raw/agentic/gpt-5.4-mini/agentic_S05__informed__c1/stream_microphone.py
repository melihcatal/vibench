from typing import AsyncIterator

from speech_client import build_live_options, create_deepgram_client
from speech_models import TranscriptChunk, normalize_transcript


async def stream_microphone(audio_source) -> AsyncIterator[TranscriptChunk]:
    client = create_deepgram_client()
    connection = await client.listen.asyncwebsocket.v("1")
    await connection.start(build_live_options())
    async for frame in audio_source:
        await connection.send(frame)
        event = await connection.receive()
        chunk = normalize_transcript(event)
        if chunk.text:
            yield chunk
    await connection.finish()
