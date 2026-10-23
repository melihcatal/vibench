import asyncio
import boto3

transcribe = boto3.client('transcribe')

async def stream_audio_chunks(audio_source):
    async for chunk in audio_source:
        response = transcribe.start_stream_transcription(
            LanguageCode='en-US',
            MediaEncoding='pcm',
            MediaSampleRate=16000,
            AudioStream=chunk
        )
        yield response