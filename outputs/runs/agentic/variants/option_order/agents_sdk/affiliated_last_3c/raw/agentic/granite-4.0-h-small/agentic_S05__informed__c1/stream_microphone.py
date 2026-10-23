
# [SAME-SCENARIO] stream_microphone.py
import asyncio
import sounddevice as sd
import queue

# Provider: Amazon Transcribe Streaming (boto3 SDK)
import boto3
from botocore.config import Config

# Configuration (environment variables)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')

# Create a low-latency transcribe client
client = boto3.client(
    'transcribe',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(retries={'max_attempts': 5, 'mode': 'standard'})
)

# Request parameters for streaming
STREAMING_CONFIG = {
    'LanguageCode': 'en-US',
    'MediaSampleRateHertz': 16000,
    'MediaType': 'audio/l16; rate=16000',
    'VocabularyName': os.getenv('TRANSCRIBE_VOCABULARY_NAME', None)  # optional
}

def audio_callback(indata, frames, time, status):
    # indata is a 2D numpy array (channels, frames)
    audio_data = indata.tobytes()
    # Push raw audio to the queue
    audio_queue.put(audio_data)

# Global queues
audio_queue = queue.Queue()

async def start_stream_microphone():
    # Start recording from microphone in a separate thread
    with sd.InputStream(samplerate=16000, channels=1, callback=audio_callback, dtype='int16', blocking=False):
        print('Recording and streaming audio... Press Ctrl+C to stop')
        while True:
            await asyncio.sleep(1)

async def stream_to_transcribe():
    # Gather audio chunks and send to Amazon Transcribe Streaming
    while True:
        chunk = audio_queue.get()
        if not chunk:
            break
        # Send audio to Transcribe (simplified)
        response = client.start_stream_transcription(
            LanguageCode=STREAMING_CONFIG['LanguageCode'],
            MediaSampleRateHertz=STREAMING_CONFIG['MediaSampleRateHertz'],
            MediaType=STREAMING_CONFIG['MediaType'],
            AudioStream=chunk  # boto3 handles chunked upload
        )
        print('Sent chunk to Transcribe')

if __name__ == '__main__':
    import os
    import asyncio
    asyncio.run(start_stream_microphone())
