import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


class SpeechClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.transcribe_client = boto3.client(
            "transcribe",
            region_name=self.region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def get_transcribe_client(self):
        return self.transcribe_client

    def validate_audio_file(self, audio_file_path: str) -> bool:
        if not os.path.exists(audio_file_path):
            return False

        valid_extensions = [".mp3", ".mp4", ".wav", ".flac", ".ogg", ".amr", ".webm"]
        _, ext = os.path.splitext(audio_file_path.lower())
        return ext in valid_extensions

    def get_job_status(self, job_name: str) -> Optional[str]:
        try:
            response = self.transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            return response["TranscriptionJob"]["TranscriptionJobStatus"]
        except ClientError as e:
            print(f"Error getting job status: {e}")
            return None

    def format_job_name(self, audio_file_path: str) -> str:
        base_name = os.path.basename(audio_file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        clean_name = "".join(
            c if c.isalnum() or c in "-_" else "_" for c in name_without_ext
        )
        return f"transcribe_{clean_name}_{os.getpid()}"
