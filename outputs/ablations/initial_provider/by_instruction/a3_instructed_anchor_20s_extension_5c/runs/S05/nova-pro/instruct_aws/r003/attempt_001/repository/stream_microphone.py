import asyncio
import boto3
from botocore.exceptions import NoCredentialsError
from speech_client import get_speech_client

async def stream_microphone():
    client = get_speech_client()
    try:
        async with client.start_stream_transcription() as stream:
            async for event in stream:
                if 'TranscriptResultStream' in event:
                    yield event['TranscriptResultStream']
    except NoCredentialsError:
        raise Exception('AWS credentials not found')