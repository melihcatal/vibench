import asyncio
import speech_client

async def stream_chunks(async_source):
    client = speech_client.get_streaming_client()
    async for chunk in async_source:
        yield client.stream_audio(chunk)
