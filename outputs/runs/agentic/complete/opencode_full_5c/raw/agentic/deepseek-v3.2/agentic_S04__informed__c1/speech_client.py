import os
import boto3
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class TranscriptionConfig:
    """Configuration for Amazon Transcribe service."""

    language_code: str = "en-US"
    media_format: str = "mp3"
    show_speaker_labels: bool = True
    max_speaker_labels: int = 10
    enable_content_redaction: bool = False
    vocabulary_name: Optional[str] = None
    bucket_name: Optional[str] = None

    @classmethod
    def from_env(cls) -> "TranscriptionConfig":
        """Create configuration from environment variables."""
        bucket_name = os.environ.get("AWS_TRANSCRIBE_BUCKET")
        language_code = os.environ.get("TRANSCRIPTION_LANGUAGE", "en-US")

        return cls(language_code=language_code, bucket_name=bucket_name)


class SpeechClient:
    """Client helper for Amazon Transcribe operations."""

    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.config = config or TranscriptionConfig.from_env()
        self.transcribe_client = boto3.client("transcribe")
        self.s3_client = boto3.client("s3") if self.config.bucket_name else None

    def upload_to_s3(self, local_path: str, object_key: str) -> str:
        """Upload audio file to S3 bucket."""
        if not self.config.bucket_name:
            raise ValueError("S3 bucket name not configured")

        self.s3_client.upload_file(local_path, self.config.bucket_name, object_key)
        return f"s3://{self.config.bucket_name}/{object_key}"

    def get_media_uri(self, audio_path: str) -> str:
        """Get S3 URI for audio file, uploading if necessary."""
        if audio_path.startswith("s3://"):
            return audio_path

        if not self.config.bucket_name:
            raise ValueError("Cannot upload local file: S3 bucket not configured")

        import uuid

        object_key = f"audio/{uuid.uuid4().hex[:8]}.{self.config.media_format}"
        return self.upload_to_s3(audio_path, object_key)

    def create_job_name(self, prefix: str = "transcription") -> str:
        """Generate a unique job name."""
        import uuid

        return f"{prefix}-{uuid.uuid4().hex[:8]}"

    def get_job_status(self, job_name: str) -> Dict[str, Any]:
        """Get status of a transcription job."""
        response = self.transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        return response["TranscriptionJob"]

    def delete_job(self, job_name: str) -> None:
        """Delete a transcription job."""
        self.transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)

    def list_jobs(self, status: Optional[str] = None, max_results: int = 100) -> list:
        """List transcription jobs, optionally filtered by status."""
        params = {"MaxResults": max_results}
        if status:
            params["Status"] = status

        response = self.transcribe_client.list_transcription_jobs(**params)
        return response["TranscriptionJobSummaries"]


def get_default_client() -> SpeechClient:
    """Get default speech client instance."""
    return SpeechClient()
