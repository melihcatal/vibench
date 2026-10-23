import asyncio
import json
import os
from typing import AsyncIterator, Optional

import websockets


DEEPGRAM_API_KEY_ENV = "DEEPGRAM_API_KEY"
DEEPGRAM_MODEL = "nova-2"
DEEPGRAM_URL = (
    "wss://api.deepgram.com/v1/listen"
    "?model={model}&interim_results=true&smart_format=true&punctuate=true"
).format(model=DEEPGRAM_MODEL)


async def stream_microphone(sample_rate: int = 16000, chunk_size: int = 3200) -> AsyncIterator[str]:
    api_key = os.environ.get(DEEPGRAM_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"{DEEPGRAM_API_KEY_ENV} is required")

    import pyaudio

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    try:
        async with websockets.connect(
            DEEPGRAM_URL,
            extra_headers={"Authorization": f"Token {api_key}"},
            ping_interval=None,
        ) as ws:

            async def send_audio() -> None:
                while True:
                    data = await asyncio.to_thread(stream.read, chunk_size, False)
                    await ws.send(data)

            sender = asyncio.create_task(send_audio())
            try:
                async for message in ws:
                    payload = json.loads(message)
                    channel = payload.get("channel", {})
                    alternatives = channel.get("alternatives", [])
                    transcript = alternatives[0].get("transcript", "") if alternatives else ""
                    if transcript and payload.get("is_final") is False:
                        yield transcript
            finally:
                sender.cancel()
                with contextlib.suppress(Exception):
                    await sender
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


async def main() -> None:
    async for transcript in stream_microphone():
        print(transcript, flush=True)


if __name__ == "__main__":
    import contextlib

    asyncio.run(main())
