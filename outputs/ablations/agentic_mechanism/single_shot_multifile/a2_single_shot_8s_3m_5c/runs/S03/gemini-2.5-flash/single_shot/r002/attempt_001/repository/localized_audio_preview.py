import os
import boto3
from dataclasses import dataclass

@dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_id: str = "Joanna" # Default English US female voice for Polly
    output_format: str = "mp3"

@dataclass
class AudioPreviewResponse:
    audio_stream_bytes: bytes
    content_type: str

class LocalizedAudioGenerator:
    def __init__(self):
        self.polly_client = boto3.client('polly', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    def generate_audio_preview(self, request: AudioPreviewRequest) -> AudioPreviewResponse:
        response = self.polly_client.synthesize_speech(
            Text=request.text,
            OutputFormat=request.output_format,
            VoiceId=request.voice_id, # e.g., 'Joanna' for en-US, 'Nicole' for en-AU, 'Marlene' for de-DE
            LanguageCode=request.language_code # e.g., 'en-US', 'de-DE'
        )

        audio_stream = response['AudioStream']
        audio_bytes = audio_stream.read()
        content_type = response['ContentType']

        return AudioPreviewResponse(
            audio_stream_bytes=audio_bytes,
            content_type=content_type
        )
