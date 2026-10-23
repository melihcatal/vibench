import boto3
from amazon_transcribe.client import TranscribeStreamingClient

class SpeechClient:
    def __init__(self, region=None):
        self.region = region or boto3.Session().region_name or "us-east-1"
        self.client = TranscribeStreamingClient(region=self.region)

    async def start_transcription_stream(self, language_code, sample_rate_hz, encoding="pcm"):
        return await self.client.start_stream_transcription(
            language_code=language_code,
            media_sample_rate_hz=sample_rate_hz,
            media_encoding=encoding
        )
