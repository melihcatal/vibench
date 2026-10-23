# [HELPER]
# speech_client.py
# Local helper that creates and configures an Amazon Transcribe Streaming client
# Provider: Amazon Transcribe Streaming (boto3 SDK)
import boto3
import json
from typing import Optional, Dict, Any

class SpeechClient:
    """Thin wrapper around the AWS Transcribe Streaming client to simplify start/stop and result handling."""

    def __init__(self):
        # Read credentials from environment; boto3 will auto‑load them.
        self.transcribe = boto3.client('transcribe')

    def start_stream(self,
                     language_code: str = 'en-US',
                     enable_punctuation: bool = False,
                     sample_rate: int = 16000,
                     encoding: str = 'pcm') -> str:
        """Start a streaming session and return the generated StreamArn."""
        start_resp = self.transcribe.start_stream_transcription(
            LanguageCode=language_code,
            EnablePunctuation=enable_punctuation,
            MediaSampleRateHertz=sample_rate,
            MediaEncoding=encoding,
        )
        stream_arn = start_resp['StreamArn']
        print(f'[SpeechClient] Stream started (ARN: {stream_arn})')
        return stream_arn

    def send_audio(self, stream_arn: str, audio_bytes: bytes):
        """Send a chunk of raw PCM audio to the running stream."""
        # boto3 client supports a synchronous send_transcript call; we wrap it.
        # In production code run this inside an executor or use an async streaming client.
        self.transcribe.send_transcript(
            StreamArn=stream_arn,
            Data=audio_bytes,
        )

    def stop_stream(self, stream_arn: str):
        """Stop the streaming session."""
        self.transcribe.stop_stream_transcription(StreamArn=stream_arn)
        print(f'[SpeechClient] Stream stopped (ARN: {stream_arn})')

    # Optional convenience callback registration
    # Users can hook into the results via custom logic or via partial_results.py

if __name__ == '__main__':
    client = SpeechClient()
    # Example: create a stream for Spanish with punctuation
    arn = client.start_stream(language_code='es-ES', enable_punctuation=True)
    # Remember to stop the stream later when finished
    # client.stop_stream(arn)