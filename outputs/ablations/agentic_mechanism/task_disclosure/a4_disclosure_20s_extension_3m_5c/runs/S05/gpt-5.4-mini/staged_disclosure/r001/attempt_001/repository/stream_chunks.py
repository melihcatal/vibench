import asyncio
import base64
import json
import os
from typing import Any, AsyncIterator, Awaitable, Callable, Optional

import websockets


AssemblyAI_WS_URL = "wss://api.assemblyai.com/v2/realtime/ws"


async def stream_audio_chunks(
    source: AsyncIterator[bytes],
    on_chunk: Callable[[bytes], Awaitable[None]],
    *,
    sample_rate: int = 16000,
    token: Optional[str] = None,
) -> None:
    auth_token = token or os.environ.get("ASSEMBLYAI_API_KEY") or os.environ.get("ASSEMBLYAI_TOKEN")
    if not auth_token:
        raise RuntimeError("Missing AssemblyAI auth token in ASSEMBLYAI_API_KEY or ASSEMBLYAI_TOKEN")

    url = f"{AssemblyAI_WS_URL}?sample_rate={sample_rate}"
    headers = {"Authorization": auth_token}

    async with websockets.connect(url, extra_headers=headers) as ws:
        async def sender() -> None:
            async for chunk in source:
                if not chunk:
                    continue
                payload = base64.b64encode(chunk).decode("ascii")
                await ws.send(json.dumps({"audio_data": payload}))
            await ws.send(json.dumps({"terminate_session": True}))

        async def receiver() -> None:
            async for message in ws:
                if isinstance(message, bytes):
                    await on_chunk(message)
                    continue
                try:
                    data: Any = json.loads(message)
                except json.JSONDecodeError:
                    continue
                audio_data = data.get("audio_data")
                if isinstance(audio_data, str) and audio_data:
                    await on_chunk(base64.b64decode(audio_data))

        await asyncio.gather(sender(), receiver())


__all__ = ["stream_audio_chunks"]
