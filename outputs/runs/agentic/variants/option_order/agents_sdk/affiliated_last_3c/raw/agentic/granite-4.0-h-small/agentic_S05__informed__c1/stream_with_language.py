
# [SAME-SCENARIO] stream_with_language.py
import os
import asyncio
import boto3
from botocore.config import Config

# Provider: Amazon Transcribe Streaming (boto3 SDK)
client = boto3.client(
    'transcribe',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(retries={'max_attempts': 5, 'mode': 'standard'})
)

LANGUAGE_CODE = os.getenv('TRANSCRIBE_LANGUAGE_CODE', 'es-ES')  # Spanish example
SAMPLE_RATE = 16000

STREAMING_CONFIG = {
    'LanguageCode': LANGUAGE_CODE,
    'MediaSampleRateHertz': SAMPLE_RATE,
    'MediaType': 'audio/l16; rate=16000',
}

def audio_callback(indata, frames, time, status):
    # Simple callback that prints received audio length (placeholder)
    print('Received audio chunk of size', len(indata.tobytes()))

async def start_stream():
    with boto3.client(
        'transcribe',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        config=Config(retries={'max_attempts': 5, 'mode': 'standard'})
    ) as client:
        # Start streaming job (simplified; real implementation uses websocket/HTTP2)
        response = client.start_stream_transcription(**STREAMING_CONFIG)
        print('Streaming session started with language:', STREAMING_CONFIG['LanguageCode'])
        # Here you would feed audio chunks to the streaming endpoint
        # For demo, we just sleep
        await asyncio.sleep(30)
    print('Streaming completed')

if __name__ == '__main__':
    import asyncio
    asyncio.run(start_stream())
