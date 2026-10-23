import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

async def stream_chunks(audio_source):
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "model": "whisper-1",
            "language": "en",
            "response_format": "text",
        }
    )

    async def chunk_generator():
        async for chunk in audio_source:
            yield chunk

    async for partial in handle_partial_results(stream):
        yield partial

    await stream.close()