import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from typing import Any, Dict, Optional


class SpeechClient:
    """Helper client for batch speech-to-text services with provider-agnostic interface.

    Currently implements Amazon Transcribe features (batch submit, get job, download transcript).
    Extend with additional providers by subclassing or adding new methods.
    """

    def __init__(self, service: str = "Amazon Transcribe") -> None:
        self.service = service
        # Initialize provider-specific client
        if service == "Amazon Transcribe":
            self._client = boto3.client(
                "transcribe",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        else:
            raise NotImplementedError(
                f"Service {service} not yet implemented in SpeechClient"
            )

    def submit_batch_transcription(self, config: Any) -> Dict[str, Any]:
        """Submit a batch transcription request.

        Args:
            config: Provider-specific configuration object (e.g., BatchTranscriptionConfig).

        Returns:
            Dict: Raw service response.
        """
        if self.service == "Amazon Transcribe":
            return self._client.start_transcription_job(**config.to_dict())
        raise NotImplementedError(f"Submit not implemented for {self.service}")

    def get_transcription_job(self, job_id: str) -> Dict[str, Any]:
        """Poll a transcription job status.

        Args:
            job_id (str): Job identifier.

        Returns:
            Dict: Raw service response.
        """
        if self.service == "Amazon Transcribe":
            return self._client.get_transcription_job(TranscriptionJobName=job_id)
        raise NotImplementedError(f"Get job not implemented for {self.service}")

    def download_transcript(self, uri: str) -> str:
        """Download transcript file from a URI (placeholder for actual download logic).

        Args:
            uri (str): Pre-signed URL or file path.

        Returns:
            str: Transcript text.
        """
        # Placeholder: in practice, fetch content via HTTP or S3. Returning a mock string.
        return "This is a placeholder transcript text."


# Helper dataclasses / plain dicts for config payloads
# These should mirror the shape required by the underlying provider SDK


class BatchTranscriptionConfig:
    """Configuration for batch transcription jobs (Amazon Transcribe example)."""

    def __init__(
        self,
        audio_file_path: str,
        job_name: Optional[str] = None,
        region: str = "us-east-1",
        enable_diarization: bool = False,
        max_speakers: int = 2,
    ) -> None:
        self.audio_file_path = audio_file_path
        self.job_name = job_name
        self.region = region
        self.enable_diarization = enable_diarization
        self.max_speakers = max_speakers

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "Media": {"MediaFileUri": self.audio_file_path},
            "TranscriptionJobName": self.job_name
            or os.path.splitext(os.path.basename(self.audio_file_path))[0],
        }
        if self.enable_diarization:
            payload["Settings"] = {
                "MaxSpeakerLabels": self.max_speakers,
                "ShowSpeakerLabels": True,
            }
        return payload
