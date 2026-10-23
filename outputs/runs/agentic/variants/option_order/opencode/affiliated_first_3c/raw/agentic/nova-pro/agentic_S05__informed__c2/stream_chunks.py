import asyncio
import aiohttp


async def stream_audio(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_any():  # type: ignore
                yield chunk
