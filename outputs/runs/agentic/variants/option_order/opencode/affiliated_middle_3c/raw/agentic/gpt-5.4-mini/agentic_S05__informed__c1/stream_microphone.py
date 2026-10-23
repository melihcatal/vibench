import asyncio
from typing import AsyncIterator

import sounddevice as sd

from speech_client import create_client, live_options, load_config
from speech_models import event_from_result


async def stream_microphone() -> AsyncIterator[str]:
    client = create_client()
    config = load_config()
    options = live_options(config)
    async with client.listen.asynclive.v("1") as connection:
        await connection.start(options)
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[bytes] = asyncio.Queue()

        def callback(indata, frames, time, status):
            loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
            while True:
                audio = await queue.get()
                await connection.send(audio)
                async for result in connection:
                    event = event_from_result(result)
                    if event.text:
                        yield event.text
                    if event.is_final:
                        break
