import boto3
import asyncio

async def stream_audio():
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text='Hello, this is a test audio stream from AWS Polly.',
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        async for chunk in response['AudioStream'].iter_chunks():
            yield chunk

async def main():
    async for chunk in stream_audio():
        print(chunk)

asyncio.run(main())