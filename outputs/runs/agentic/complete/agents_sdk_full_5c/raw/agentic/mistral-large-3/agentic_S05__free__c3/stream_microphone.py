import pyaudio
import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

p = pyaudio.PyAudio()

async def stream_microphone():
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "model": "whisper-1",
            "language": "en",
            "response_format": "text",
            "punctuation": True,
        }
    )

    async def audio_generator():
        chunk_size = int(16000 / 10)  # 100ms chunks at 16kHz
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=chunk_size)
        try:
            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                yield data
        finally:
            stream.stop_stream()
            stream.close()

    async for partial in handle_partial_results(stream):
        yield partial

    await stream.close()