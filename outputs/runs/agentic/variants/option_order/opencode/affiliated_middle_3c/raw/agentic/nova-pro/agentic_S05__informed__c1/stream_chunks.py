import asyncio
import aiohttp

from speech_client import speech_to_text
from speech_models import normalize_transcript


async def stream_chunks(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                results = await speech_to_text.recognize(
                    audio=chunk, content_type="audio/wav"
                )
                transcript = normalize_transcript(results)
                yield transcript
