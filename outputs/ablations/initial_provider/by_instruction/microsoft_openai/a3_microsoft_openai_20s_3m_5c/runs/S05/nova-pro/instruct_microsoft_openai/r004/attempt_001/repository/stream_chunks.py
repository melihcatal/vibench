import asyncio

async def stream_chunks():
    async for chunk in get_audio_chunks():
        yield chunk

async def get_audio_chunks():
    # Simulate async audio chunk retrieval
    for i in range(5):
        await asyncio.sleep(1)
        yield b'audio_chunk_%d' % i