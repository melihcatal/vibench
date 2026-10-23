import asyncio
from typing import AsyncIterator, Awaitable, Callable, Optional

import websockets


ASSEMBLYAI_STREAMING_URL = "wss://api.assemblyai.com/v2/realtime/ws"


async def stream_chunks(
    audio_source: AsyncIterator[bytes],
    send_audio: Callable[[bytes], Awaitable[None]],
    *,
    close_after: Optional[bool] = True,
) -> None:
    async for chunk in audio_source:
        if not chunk:
            continue
        await send_audio(chunk)
    if close_after:
        await asyncio.sleep(0)


async def stream_chunks_via_assemblyai(
    audio_source: AsyncIterator[bytes],
    api_key: str,
) -> None:
    headers = {"Authorization": api_key}
    async with websockets.connect(ASSEMBLYAI_STREAMING_URL, extra_headers=headers) as ws:
        async def send_audio(chunk: bytes) -> None:
            await ws.send(chunk)

        await stream_chunks(audio_source, send_audio)
