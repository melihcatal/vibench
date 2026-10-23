import asyncio
from typing import AsyncIterator

import pyaudio

from speech_client import build_live_options, get_deepgram_client
from speech_models import SpeechStreamConfig, normalize_transcript


async def microphone_audio(
    rate: int = 16000, chunk_size: int = 1024
) -> AsyncIterator[bytes]:
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            yield stream.read(chunk_size, exception_on_overflow=False)
            await asyncio.sleep(0)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


async def stream_microphone() -> AsyncIterator[str]:
    client = get_deepgram_client()
    conn = await client.listen.asyncwebsocket.v("1")
    await conn.start(build_live_options(SpeechStreamConfig()))
    async for frame in microphone_audio():
        await conn.send(frame)
        event = await conn.receive()
        if event:
            yield normalize_transcript(event).text
