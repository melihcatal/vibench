import asyncio
import json
from typing import AsyncIterator

import websockets

from speech_client import load_config
from speech_models import TranscriptEvent, normalize_transcript


async def stream_microphone_audio() -> AsyncIterator[TranscriptEvent]:
    config = load_config()
    async with websockets.connect(
        config.assemblyai_realtime_url,
        extra_headers={"Authorization": config.assemblyai_api_key},
    ) as ws:
        await ws.send(json.dumps({"sample_rate": 16000}))
        while True:
            message = await ws.recv()
            payload = json.loads(message)
            event = normalize_transcript(payload)
            if event.text:
                yield event


async def main() -> None:
    async for event in stream_microphone_audio():
        if event.is_final:
            print(event.text)
        else:
            print(event.text, end="\r")


if __name__ == "__main__":
    asyncio.run(main())
