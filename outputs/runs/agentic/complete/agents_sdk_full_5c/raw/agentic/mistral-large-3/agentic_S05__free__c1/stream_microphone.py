import pyaudio
import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

p = pyaudio.PyAudio()

async def stream_microphone():
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "config": {
                "encoding": "LINEAR16",
                "sample_rate_hertz": 16000,
                "language_code": "en-US",
                "model": "latest_long",
                "enable_automatic_punctuation": True,
            },
            "single_utterance": False,
        }
    )

    async def audio_generator():
        loop = asyncio.get_event_loop()
        audio_interface = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
            stream_callback=lambda in_data, frame_count, time_info, status: in_data,
        )
        audio_interface.start_stream()
        try:
            while True:
                in_data = await loop.run_in_executor(None, audio_interface.read, 1024, False)
                yield in_data
        finally:
            audio_interface.stop_stream()
            audio_interface.close()

    await stream.write(audio_generator())
    async for response in stream:
        await handle_partial_results(response)