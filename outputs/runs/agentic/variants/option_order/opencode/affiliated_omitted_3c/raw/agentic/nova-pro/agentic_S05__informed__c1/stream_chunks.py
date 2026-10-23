import asyncio
import aiohttp
import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))


async def stream_chunks():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/audio_stream") as resp:
            async for chunk in resp.content.iter_chunked(1024):
                yield chunk
