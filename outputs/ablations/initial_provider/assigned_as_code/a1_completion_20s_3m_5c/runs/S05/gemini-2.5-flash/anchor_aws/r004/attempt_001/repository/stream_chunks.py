import asyncio

import boto3

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.model import TranscriptResultStream

async def stream_chunks(audio_chunks, config=None):
    config = config or {}
    client = TranscribeStreamingClient(region=config.get("region") or boto3.Session().region_name or "us-east-1")
    stream = await client.start_stream_transcription(
        language_code=config.get("language_code", "en-US"),
        media_sample_rate_hz=config.get("sample_rate_hz", 16000),
        media_encoding="pcm"
    )

    async def send_audio():
        try:
            for chunk in audio_chunks:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await stream.input_stream.end_stream()

    sender = asyncio.create_task(send_audio())
    try:
        async for event in stream.output_stream:
            for result in event.transcript.results:
                if result.alternatives:
                    yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial}
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)
