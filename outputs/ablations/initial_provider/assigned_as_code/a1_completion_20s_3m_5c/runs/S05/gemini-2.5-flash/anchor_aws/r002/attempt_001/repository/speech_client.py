import boto3
from amazon_transcribe.client import TranscribeStreamingClient

class SpeechClient:
    def __init__(self, region: str = None):
        self.region = region or boto3.Session().region_name or "us-east-1"
        self._client = None

    async def get_client(self) -> TranscribeStreamingClient:
        if self._client is None:
            self._client = TranscribeStreamingClient(region=self.region)
        return self._client
