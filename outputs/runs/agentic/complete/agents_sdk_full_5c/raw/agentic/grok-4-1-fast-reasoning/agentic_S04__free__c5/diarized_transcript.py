import time
import uuid
from typing import Optional

from speech_client import get_transcribe_client, upload_audio_to_s3, S3_BUCKET

def request_diarized_transcription(
    audio_file: str,
    job_name: Optional[str] = None,
    language_code: str = 'en-US',
    media_format: str = 'wav',
    max_speakers: int = 10
) -> str:
    if job_name is None:
        job_name = f"diarize-{uuid.uuid4().hex[:8]}-{int(time.time())}"
    s3_key = f"{job_name}.{media_format}"
    media_file_uri = upload_audio_to_s3(audio_file, s3_key)
    client = get_transcribe_client()
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat=media_format,
        Media={'MediaFileUri': media_file_uri},
        OutputBucketName=S3_BUCKET,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': max_speakers
        }
    )
    return job_name