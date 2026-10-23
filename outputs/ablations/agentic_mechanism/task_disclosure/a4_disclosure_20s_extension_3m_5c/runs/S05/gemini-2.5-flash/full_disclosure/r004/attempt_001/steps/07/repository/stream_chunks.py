import asyncio
from google.cloud import speech_v1p1beta1 as speech

async def stream_audio_chunks(audio_source):
    """
    Streams audio chunks from an asynchronous source and yields StreamingRecognizeRequest objects.
    
    Args:
        audio_source: An asynchronous generator or iterable that yields audio chunks (bytes).
    
    Yields:
        speech.StreamingRecognizeRequest: Request objects containing audio content.
    """
    async for chunk in audio_source:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

