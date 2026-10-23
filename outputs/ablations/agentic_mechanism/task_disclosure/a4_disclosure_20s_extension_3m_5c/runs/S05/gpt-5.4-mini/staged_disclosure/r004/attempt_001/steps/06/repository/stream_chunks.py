import asyncio
import base64
import contextlib
import json
import os
from typing import Any, AsyncIterator, AsyncIterable, Dict, Optional

import websockets


OPENAI_REALTIME_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview"


async def _iterate_async_source(source: AsyncIterable[bytes]) -> AsyncIterator[bytes]:
    async for chunk in source:
        if chunk:
            yield chunk


async def stream_audio_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[bytes]:
    api_key = os.environ["OPENAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "realtime=v1",
    }
    async with websockets.connect(OPENAI_REALTIME_URL, extra_headers=headers) as ws:
        await ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "turn_detection": {"type": "server_vad"},
                        "input_audio_format": "pcm16",
                        "modalities": ["audio"],
                    },
                }
            )
        )

        async def send_audio() -> None:
            async for chunk in _iterate_async_source(source):
                await ws.send(
                    json.dumps(
                        {
                            "type": "input_audio_buffer.append",
                            "audio": base64.b64encode(chunk).decode("ascii"),
                        }
                    )
                )
            await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
            await ws.send(json.dumps({"type": "response.create"}))

        sender = asyncio.create_task(send_audio())
        try:
            async for message in ws:
                event = json.loads(message)
                event_type = event.get("type", "")
                if event_type in ("response.audio.delta", "response.output_audio.delta"):
                    audio_b64 = event.get("delta", "") or event.get("audio", "")
                    if audio_b64:
                        yield base64.b64decode(audio_b64)
                elif event_type in ("response.audio.done", "response.completed"):
                    break
        finally:
            sender.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await sender


async def main() -> None:
    async def demo_source() -> AsyncIterator[bytes]:
        for _ in range(3):
            yield b"\x00\x00" * 1024
            await asyncio.sleep(0.01)

    async for chunk in stream_audio_chunks(demo_source()):
        print(len(chunk), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
