import asyncio
import boto3

polly_client = boto3.client('polly')

async def stream_audio(text):
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    if 'AudioStream' in response:
        async for chunk in response['AudioStream'].iter_chunks():
            yield chunk
    else:
        raise ValueError('AudioStream not found in response')

async def main():
    async for chunk in stream_audio('Hello, this is an audio stream from AWS Polly'):
        # Here you would typically send the chunk to an audio output
        print(chunk)

asyncio.run(main())