from __future__ import annotations

import os
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

import aiohttp


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[bytes]:
    url = os.environ.get("OPENAI_TRANSCRIBE_STREAM_CHUNKS_URL", "https://api.openai.com/v1/audio/transcriptions")
    api_key = os.environ.get("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    async with aiohttp.ClientSession(headers=headers) as session:
        async for chunk in source:
            if not chunk:
                continue
            async with session.post(url, data=chunk) as response:
                response.raise_for_status()
                await response.read()
            yield chunk
