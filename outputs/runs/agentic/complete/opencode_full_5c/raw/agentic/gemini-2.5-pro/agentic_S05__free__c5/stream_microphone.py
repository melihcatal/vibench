import asyncio
import pyaudio
from google.cloud import speech
from speech_client import get_speech_client, get_streaming_config

RATE = 16000
CHUNK = int(RATE / 10)


async def stream_microphone():
    client = get_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=get_streaming_config(),
        interim_results=True,
    )

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    async def audio_generator():
        while True:
            data = audio_stream.read(CHUNK)
            yield speech.StreamingRecognizeRequest(audio_content=data)
            await asyncio.sleep(0.1)

    requests = audio_generator()
    responses = await client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript

    audio_stream.stop_stream()
    audio_stream.close()
    audio_interface.terminate()
