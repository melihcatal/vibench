import asyncio
import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


async def stream_audio_chunks():
    async for chunk in get_audio_chunks():
        response = transcribe_client.start_stream_transcription(
            LanguageCode="en-US",
            MediaEncoding="pcm",
            MediaSampleRateHertz=16000,
            StreamName="audio-chunks-stream",
            AudioStream=chunk,
        )
        yield response["TranscriptionJob"]["TranscriptionJobName"]
