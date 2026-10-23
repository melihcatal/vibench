import asyncio
from typing import AsyncIterable, AsyncIterator, Optional

import aiohttp


GOOGLE_CLOUD_SPEECH_V1_STREAMING_RECOGNIZE_URL = "https://speech.googleapis.com/v1/speech:recognize"


async def stream_chunks(source: AsyncIterable[bytes], timeout: Optional[float] = None) -> AsyncIterator[bytes]:
    async for chunk in source:
        if chunk:
            yield chunk


async def transcribe_google_stream(audio_source: AsyncIterable[bytes], api_key: str) -> str:
    payload = {
        "config": {
            "encoding": "LINEAR16",
            "languageCode": "en-US",
            "model": "latest_long",
            "enableAutomaticPunctuation": True,
        },
        "audio": {"content": ""},
    }
    buffered = bytearray()
    async for chunk in stream_chunks(audio_source):
        buffered.extend(chunk)
    if buffered:
        payload["audio"]["content"] = buffered.hex()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            GOOGLE_CLOUD_SPEECH_V1_STREAMING_RECOGNIZE_URL,
            params={"key": api_key},
            json=payload,
            timeout=timeout,
        ) as response:
            response.raise_for_status()
            data = await response.json()
    results = data.get("results", [])
    if not results:
        return ""
    alternatives = results[0].get("alternatives", [])
    if not alternatives:
        return ""
    return alternatives[0].get("transcript", "")
