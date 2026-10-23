import os
import boto3
from botocore.exceptions import ClientError
from typing import Any, Dict

# Configuration for Amazon Transcribe via environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


class SpeechClient:
    """Local helper that wraps boto3 Amazon Transcribe client with simple utilities."""

    def __init__(self):
        self.transcribe = boto3.client("transcribe", region_name=AWS_REGION)

    def create_batch_transcription_payload(
        self, audio_file_path: str, job_name: str
    ) -> Dict[str, Any]:
        """Builds the request dict for a batch transcription job."""
        return {
            "TranscriptionJobName": job_name,
            "LanguageCode": "en-US",
            "Media": {"MediaFileUri": f"file://{audio_file_path}"},
            "OutputBucketName": os.getenv(
                "AWS_OUTPUT_BUCKET"
            ),  # optionally set via env
        }

    def create_diarized_transcription_payload(
        self, audio_file_path: str, job_name: str, max_speakers: int
    ) -> Dict[str, Any]:
        """Builds a payload enabling speaker diarization."""
        payload = self.create_batch_transcription_payload(audio_file_path, job_name)
        payload.update(
            {"Settings": {"ShowSpeakerLabels": True, "MaxSpeakerLabels": max_speakers}}
        )
        return payload

    def start_transcription_job(
        self, job_name: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Starts the job; wraps boto3 call and returns raw response."""
        return self.transcribe.start_transcription_job(
            TranscriptionJobName=job_name, **payload
        )

    def get_transcription_job(self, job_name: str) -> Dict[str, Any]:
        """Polls a transcription job and returns its current status response."""
        return self.transcribe.get_transcription_job(TranscriptionJobName=job_name)
