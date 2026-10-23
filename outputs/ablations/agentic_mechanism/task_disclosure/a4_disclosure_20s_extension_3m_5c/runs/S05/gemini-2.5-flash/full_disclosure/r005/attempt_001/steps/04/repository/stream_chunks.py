
from google.cloud import speech

async def stream_audio_chunks(audio_source):
    """
    Streams audio chunks from an asynchronous audio source.

    Args:
        audio_source: An asynchronous generator or iterable that yields audio bytes.

    Yields:
        bytes: Audio chunks.
    """
    async for chunk in audio_source:
        yield chunk

