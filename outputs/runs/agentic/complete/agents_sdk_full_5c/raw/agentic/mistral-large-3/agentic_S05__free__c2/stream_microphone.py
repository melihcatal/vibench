import pyaudio
import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_result

# Google Cloud Speech-to-Text streaming config
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

async def stream_microphone():
    client = get_speech_client()
    config = {
        "config": {
            "encoding": "LINEAR16",
            "sample_rate_hertz": RATE,
            "language_code": "en-US",
            "model": "latest_long",
            "enable_automatic_punctuation": True,
        },
        "single_utterance": False,
    }

    stream = client.streaming_recognize(config, handle_partial_result)
    p = pyaudio.PyAudio()
    stream_audio = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream_audio.read(CHUNK, exception_on_overflow=False)
            await stream.send(data)
    except asyncio.CancelledError:
        stream_audio.stop_stream()
        stream_audio.close()
        p.terminate()
        await stream.close()