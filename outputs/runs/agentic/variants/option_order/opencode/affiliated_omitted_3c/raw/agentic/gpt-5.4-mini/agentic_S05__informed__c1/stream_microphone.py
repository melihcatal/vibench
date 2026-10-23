import asyncio
from typing import AsyncIterator

from deepgram import DeepgramClient, LiveOptions

from speech_client import load_speech_config
from speech_models import TranscriptChunk, transcript_chunk_from_deepgram


async def stream_microphone_audio() -> AsyncIterator[bytes]:
    while True:
        await asyncio.sleep(0.02)
        yield b""


async def stream_microphone_transcripts() -> AsyncIterator[TranscriptChunk]:
    config = load_speech_config()
    client = DeepgramClient(config.api_key)
    dg = client.listen.asyncwebsocket.v("1")
    options = LiveOptions(
        model="nova-2",
        language=config.language_code,
        punctuate=config.punctuation,
        interim_results=True,
    )

    async def _audio() -> AsyncIterator[bytes]:
        async for chunk in stream_microphone_audio():
            yield chunk

    async with dg.start(options) as connection:
        async for chunk in _audio():
            await connection.send(chunk)
            if connection.received:
                for message in connection.received:
                    yield transcript_chunk_from_deepgram(message)
