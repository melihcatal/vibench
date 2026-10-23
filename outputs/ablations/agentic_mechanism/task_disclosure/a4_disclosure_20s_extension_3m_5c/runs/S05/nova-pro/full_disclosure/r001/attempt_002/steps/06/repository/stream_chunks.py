import asyncio
import boto3

transcribe = boto3.client('transcribe', region_name='us-west-2')

async def stream_audio_chunks(audio_source):
    async for chunk in audio_source:
        await process_audio_chunk(chunk)

async def process_audio_chunk(chunk):
    response = transcribe.start_stream_transcription(
        LanguageCode='en-US',
        MediaEncoding='pcm',
        MediaSampleRateHertz=16000,
        StreamURL='https://your-stream-url'
    )
    print(response)