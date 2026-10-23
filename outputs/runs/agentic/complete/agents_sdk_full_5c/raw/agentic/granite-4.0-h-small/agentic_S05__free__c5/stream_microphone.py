# stream_microphone.py
import asyncio, warnings, os, json
import grpc
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from google.auth.exceptions import DefaultCredentialsError

# Helper client utilities are imported from local helpers.
from speech_client import get_speech_client, DEFAULT_LANG
from speech_models import StreamResponseHandler

async def stream_microphone():
    """Continuously streams audio from the microphone and yields interim transcripts.
    Uses Google Cloud Speech-to-Text (v1p1beta1) streaming API.
    """
    try:
        client = get_speech_client()
    except DefaultCredentialsError:
        warnings.warn("Google Cloud credentials not found.")
        return

    config = types.StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=DEFAULT_LANG,
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )

    # Set up audio generator that reads from the default microphone.
    # pip install sounddevice aiohttp to use asyncio-friendly microphone stream.
    import sounddevice as sd
    import asyncio
    import numpy as np

    async def audio_generator():
        # Record in blocks of 1024 samples (~0.064s at 16kHz)
        stream = sd.InputStream(callback=lambda out_data, frame_count, time, status: out_data,
                                 samplerate=16000, channels=1, blocksize=1024, dtype='float32')
        async with stream:
            while True:
                try:
                    data = await loop.run_in_executor(None, stream.read, 1024)
                    # Convert to bytes in 16-bit PCM format
                    yield data.tobytes()
                except sd.PortAudioError:
                    break

    loop = asyncio.get_event_loop()
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in audio_generator())

    try:
        responses = client.streaming_recognize(config, requests)
        handler = StreamResponseHandler()
        async for resp in responses:
            for result in resp.results:
                if result.is_final:
                    handler.final(result)
                else:
                    handler.interim(result)
                if result.alternatives:
                    yield result.alternatives[0].transcript
    except Exception as e:
        print(f"Streaming error: {e}")

if __name__ == "__main__":
    async def main():
        async for text in stream_microphone():
            print("Interim: " + text)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
