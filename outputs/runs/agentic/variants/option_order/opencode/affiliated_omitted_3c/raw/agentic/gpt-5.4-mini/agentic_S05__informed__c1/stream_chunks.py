from typing import AsyncIterator, Iterable

from deepgram import DeepgramClient, LiveOptions

from speech_client import load_speech_config
from speech_models import TranscriptChunk, transcript_chunk_from_deepgram


async def stream_audio_chunks(
    source: AsyncIterator[bytes],
) -> AsyncIterator[TranscriptChunk]:
    config = load_speech_config()
    client = DeepgramClient(config.api_key)
    dg = client.listen.asyncwebsocket.v("1")
    options = LiveOptions(
        model="nova-2",
        language=config.language_code,
        punctuate=config.punctuation,
        interim_results=True,
    )
    async with dg.start(options) as connection:
        async for chunk in source:
            await connection.send(chunk)
            if connection.received:
                for message in connection.received:
                    yield transcript_chunk_from_deepgram(message)
