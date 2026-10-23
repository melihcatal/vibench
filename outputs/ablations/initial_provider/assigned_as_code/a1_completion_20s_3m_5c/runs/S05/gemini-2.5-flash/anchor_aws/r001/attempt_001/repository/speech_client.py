import asyncio
import boto3
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.model import TranscriptResultStream, StartStreamTranscriptionRequest
from typing import AsyncIterable

class AWSStreamClient:
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.client = TranscribeStreamingClient(region=self.region)

    async def start_transcription_stream(
        self, language_code: str, sample_rate_hz: int
    ) -> TranscriptResultStream:
        return await self.client.start_stream_transcription(
            language_code=language_code,
            media_sample_rate_hz=sample_rate_hz,
            media_encoding="pcm",
        )

    async def generate_audio_events(self, audio_chunks: AsyncIterable[bytes], input_stream):
        try:
            async for chunk in audio_chunks:
                await input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await input_stream.end_stream()

