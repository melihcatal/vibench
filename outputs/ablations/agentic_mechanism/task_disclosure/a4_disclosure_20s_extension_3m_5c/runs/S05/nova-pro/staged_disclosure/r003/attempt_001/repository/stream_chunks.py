import asyncio
import boto3

polly_client = boto3.client('polly')

async def stream_audio_chunks(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        async for chunk in response['AudioStream'].iter_chunks():
            yield chunk
    else:
        raise Exception('AudioStream not found in response')

async def main():
    text = 'Hello, this is a test stream from Amazon Polly.'
    async for chunk in stream_audio_chunks(text):
        print(chunk)

asyncio.run(main())