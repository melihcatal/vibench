import asyncio
import aiohttp
import pyaudio

# Google Cloud Speech-to-Text 
from google.cloud import speech_v1p1beta1 as speech

# Helper utilities from local modules
from speech_client import get_speech_client
from speech_models import StreamingRecognizeRequest

# Configuration (could be loaded from env vars or config file)
LANGUAGE_CODE = "en-US"
SAMPLE_RATE_HZ = 16000
CHUNK_SIZE = 1024  # bytes
INTERIM_RESULTS = True

async def audio_generator():
    """Yield audio chunks from the microphone using PyAudio."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=SAMPLE_RATE_HZ,
                     input=True,
                     frames_per_buffer=CHUNK_SIZE)
    try:
        while True:
            data = stream.read(CHUNK_SIZE)
            yield data
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def stream_microphone():
    """Stream microphone audio to Google Cloud STT and print interim transcripts."""
    client = get_speech_client()
    audio_gen = audio_generator()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE_HZ,
        language_code=LANGUAGE_CODE,
        enable_automatic_punctuation=INTERIM_RESULTS,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=INTERIM_RESULTS,
    )
    requests = [
        StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_gen
    ]
    # Send requests asynchronously
    async with client.streaming_recognize(streaming_config, requests) as response_stream:
        async for result in response_stream:
            if result.results:
                for r in result.results:
                    if r.alternatives:
                        transcript = r.alternatives[0].transcript
                        is_final = r.is_final
                        print(f"{"INTERIM" if not is_final else "FINAL"}: {transcript}")

if __name__ == "__main__":
    asyncio.run(stream_microphone())