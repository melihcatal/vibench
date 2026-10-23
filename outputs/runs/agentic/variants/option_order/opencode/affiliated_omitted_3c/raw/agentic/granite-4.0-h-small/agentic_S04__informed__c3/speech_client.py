# Local helper utilities for Batch Speech-to-Text
import os
import boto3
import time


class TranscribeClient:
    def __init__(self):
        self.client = boto3.client(
            "transcribe",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def submit(self, job_name, audio_file_path, language_code="en-US"):
        """Submit an audio file for batch transcription. Returns job name."""
        self.client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": f"s3://{os.getenv('S3_BUCKET')}/{audio_file_path}"},
            MediaFormat="mp3",
            LanguageCode=language_code,
        )
        return job_name

    def poll(self, job_name, interval=10):
        """Poll the transcription job for completion. Returns transcript URI."""
        while True:
            resp = self.client.get_transcription_job(TranscriptionJobName=job_name)
            status = resp["TranscriptionJob"]["TranscriptionJobStatus"]
            if status == "COMPLETED":
                return resp["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            if status == "FAILED":
                raise RuntimeError(
                    f"Failed: {resp['TranscriptionJob']['FailureReason']}"
                )
            print(f"Status {status}. Waiting {interval}s...")
            time.sleep(interval)

    def diarize(
        self, job_name, audio_uri, language_code="en-US", diarization_config=None
    ):
        """Submit a job with speaker diarization."""
        self.client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            Media={"MediaFileUri": audio_uri},
            MediaFormat="mp3",
            Settings={"DiarizationConfig": diarization_config},
        )
        return job_name

    def timestamp(self, job_name):
        """Placeholder - assume timestamps are enabled in the transcription job settings."""
        pass


# Singleton helper instance
transcribe = TranscribeClient()
