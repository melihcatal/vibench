import asyncio
import json
from typing import AsyncIterable, AsyncIterator

import websockets

from speech_client import load_config
from speech_models import StreamingAudioChunk, TranscriptEvent, normalize_transcript


async def stream_audio_chunks(
    chunks: AsyncIterable[StreamingAudioChunk],
) -> AsyncIterator[TranscriptEvent]:
    config = load_config()
    async with websockets.connect(
        config.assemblyai_realtime_url,
        extra_headers={"Authorization": config.assemblyai_api_key},
    ) as ws:
        await ws.send(json.dumps({"sample_rate": 16000}))

        async def sender() -> None:
            async for chunk in chunks:
                await ws.send(chunk.data)
            await ws.send(json.dumps({"terminate_session": True}))

        sender_task = asyncio.create_task(sender())
        try:
            while True:
                message = await ws.recv()
                event = normalize_transcript(json.loads(message))
                if event.text:
                    yield event
        finally:
            sender_task.cancel()
