import asyncio
import pyaudio
import os
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from typing import AsyncGenerator
from speech_client import DEEPGRAM_API_KEY

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 320


async def stream_with_language(
    language: str = "en", punctuate: bool = True
) -> AsyncGenerator[str, None]:
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY not set")

    client = DeepgramClient(DEEPGRAM_API_KEY)
    connection = client.listen.live.v("1")

    result_queue = asyncio.Queue()

    def transcript_callback(result, **kwargs):
        transcript = ""
        if (
            hasattr(result, "channel")
            and result.channel
            and result.channel.alternatives
        ):
            transcript = result.channel.alternatives[0].transcript.strip()
        is_final = getattr(result, "is_final", False)
        result_queue.put_nowait({"transcript": transcript, "is_final": is_final})

    connection.on(LiveTranscriptionEvents.Transcript, transcript_callback)

    await connection.start(
        LiveOptions(
            model="nova-2", language=language, punctuate=punctuate, smart_format=True
        )
    )

    p = pyaudio.PyAudio()
    audio_stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    try:
        while True:
            data = audio_stream.read(CHUNK, exception_on_overflow=False)
            connection.send(data)

            while True:
                try:
                    res = result_queue.get_nowait()
                    yield res["transcript"]
                except asyncio.QueueEmpty:
                    break
            await asyncio.sleep(0)
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        await connection.finish()
