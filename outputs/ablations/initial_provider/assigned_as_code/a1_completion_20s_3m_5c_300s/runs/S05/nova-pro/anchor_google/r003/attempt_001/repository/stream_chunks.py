import asyncio
import aiohttp

async def stream_audio_chunks(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                yield chunk