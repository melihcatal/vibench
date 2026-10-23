import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError

from speech_models import TranscriptionJobRequest, TranscriptionJobResponse


class SpeechClient:
    def __init__(self):
        self.client = boto3.client(
            "transcribe",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def submit_transcription_job(
        self, request: TranscriptionJobRequest
    ) -> TranscriptionJobResponse:
        try:
            response = self.client.start_transcription_job(
                TranscriptionJobName=request.job_name,
                LanguageCode=request.language_code,
                Media={"MediaFileUri": request.media_uri},
                MediaFormat=request.media_format,
                OutputBucketName=request.output_bucket,
                Settings={
                    "ShowSpeakerLabels": request.show_speaker_labels,
                    "MaxSpeakerLabels": request.max_speaker_labels,
                    "ChannelIdentification": request.channel_identification,
                }
                if request.show_speaker_labels
                else {},
            )
            return TranscriptionJobResponse(
                job_name=response["TranscriptionJob"]["TranscriptionJobName"],
                job_status=response["TranscriptionJob"]["TranscriptionJobStatus"],
                job_id=response["TranscriptionJob"]["TranscriptionJobName"],
            )
        except ClientError as e:
            raise Exception(f"Failed to submit transcription job: {e}")
