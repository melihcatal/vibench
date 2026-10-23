import asyncio
import aiohttp

from speech_client import speech_to_text


async def stream_chunks(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                yield chunk


async def main():
    async for chunk in stream_chunks("https://example.com/audio_stream"):
        await speech_to_text.send_audio_data(chunk)


asyncio.run(main())
