
# [SAME-SCENARIO] stream_chunks.py
import asyncio
import aiohttp
import queue

# Provider: Google Cloud Speech-to-Text streaming (google-cloud-speech SDK)
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

# Configuration (environment variables)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SESSION_ID = 'session-1'
LANGUAGE_CODE = 'en-US'
SAMPLE_RATE_HZ = 16000

client = speech.SpeechClient()

# Request config for streaming
config = types.StreamingRecognitionConfig(
    config=types.RecognitionConfig(
        language_code=LANGUAGE_CODE,
        encoding='LINEAR16',
        sample_rate_hertz=SAMPLE_RATE_HZ,
    ),
    interim_results=True,
)

# Global queues
audio_queue = queue.Queue()

async def capture_audio_chunks():
    # Placeholder for actual audio capture; in practice use an async audio source (e.g., PyAudio, sounddevice)
    # Here we just simulate chunk generation.
    for _ in range(5):
        chunk = b'\x00' * 640  # 20ms of 16kHz 16-bit mono silence
        audio_queue.put(chunk)
        await asyncio.sleep(0.02)

async def stream_audio_to_google():
    # Create a streaming call
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in iter(audio_queue.get, None))
    responses = client.streaming_recognize(config, requests)
    async for response in responses:
        await handle_response(response)

async def handle_response(response):
    for result in response.results:
        if result.is_final:
            print('Final transcript:', result.alternatives[0].transcript)
        else:
            print('Interim transcript:', result.alternatives[0].transcript)

async def main():
    await asyncio.gather(capture_audio_chunks(), stream_audio_to_google())

if __name__ == '__main__':
    asyncio.run(main())
