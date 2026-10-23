from typing import AsyncIterator

from speech_client import SpeechConfig, create_deepgram_client
from speech_models import TranscriptChunk, normalize_transcript


async def stream_with_language(
    audio_source, language: str = "en-US", punctuate: bool = True
) -> AsyncIterator[TranscriptChunk]:
    config = SpeechConfig(
        api_key=create_deepgram_client().config.api_key,
        language=language,
        punctuate=punctuate,
    )
    client = create_deepgram_client(config)
    connection = await client.listen.asyncwebsocket.v("1")
    options = {
        "model": config.model,
        "language": language,
        "punctuate": punctuate,
        "interim_results": True,
    }
    await connection.start(options)
    async for frame in audio_source:
        await connection.send(frame)
        event = await connection.receive()
        chunk = normalize_transcript(event)
        if chunk.text:
            yield chunk
    await connection.finish()
