import asyncio
from google.cloud import speech

async def generate_audio_requests(audio_stream):
    async for chunk in audio_stream:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)