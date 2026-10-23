import asyncio
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

transcribe = boto3.client('transcribe')

async def stream_audio_chunks(audio_stream):
    try:
        async for chunk in audio_stream:
            response = transcribe.start_stream_transcription(
                LanguageCode='en-US',
                MediaEncoding='pcm',
                MediaSampleRate=16000,
                AudioStream=chunk
            )
            yield response
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
    except Exception as e:
        print(f'Error streaming audio: {e}')
