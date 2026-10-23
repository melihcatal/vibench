import os
import uuid

from speech_client import get_transcribe_client


def submit_transcription(audio_uri: str, language_code: str = "en-US"):
    client = get_transcribe_client()
    job_name = f"batch-transcription-{uuid.uuid4().hex}"
    return client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_uri},
        MediaFormat=os.getenv("TRANSCRIBE_MEDIA_FORMAT", "mp3"),
        LanguageCode=language_code,
    )
