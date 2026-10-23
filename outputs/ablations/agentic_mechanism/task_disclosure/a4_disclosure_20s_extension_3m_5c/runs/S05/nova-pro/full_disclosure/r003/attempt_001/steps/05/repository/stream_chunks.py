import asyncio
import boto3

transcribe_client = boto3.client('transcribestreaming')

async def stream_audio_chunks(audio_source):
    async for chunk in audio_source:
        await transcribe_client.start_stream_transcription(AudioStream=chunk)
        yield chunk