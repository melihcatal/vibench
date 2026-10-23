import pyaudio
import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

async def stream_microphone():
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "config": {
                "encoding": "LINEAR16",
                "sample_rate_hertz": RATE,
                "language_code": "en-US",
                "model": "latest_long",
                "enable_automatic_punctuation": True,
            },
            "single_utterance": False,
        }
    )

    async def audio_generator():
        audio_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        try:
            while True:
                data = audio_stream.read(CHUNK, exception_on_overflow=False)
                yield data
                await asyncio.sleep(0.01)
        finally:
            audio_stream.stop_stream()
            audio_stream.close()

    await stream.write(audio_generator())
    async for response in stream:
        await handle_partial_results(response)

    p.terminate()