import asyncio
import boto3

polly_client = boto3.client('polly')

async def stream_audio(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        async for chunk in response['AudioStream'].iter_chunks():
            yield chunk

async def main():
    async for chunk in stream_audio('Hello, this is a test audio stream.'):
        print(chunk)

asyncio.run(main())