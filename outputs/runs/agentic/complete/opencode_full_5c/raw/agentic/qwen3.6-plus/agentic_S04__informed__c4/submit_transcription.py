import os
from speech_client import create_transcription_job, upload_audio_file
from speech_models import (
    TranscriptionRequest,
    TranscriptionJob,
    TranscriptionStatus,
    normalize_assemblyai_response,
)


def submit_transcription(
    audio_file_path: str = None,
    audio_url: str = None,
    language_code: str = "en",
) -> TranscriptionJob:
    if audio_file_path:
        audio_url = upload_audio_file(audio_file_path)
    elif not audio_url:
        raise ValueError("Either audio_file_path or audio_url must be provided")

    job_response = create_transcription_job(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=False,
        word_timestamps=False,
    )

    job = TranscriptionJob(
        job_id=job_response["id"],
        status=TranscriptionStatus.QUEUED,
        audio_url=audio_url,
    )
    return job


if __name__ == "__main__":
    audio_path = os.environ.get("AUDIO_FILE_PATH")
    url = os.environ.get("AUDIO_URL")
    lang = os.environ.get("LANGUAGE_CODE", "en")
    result = submit_transcription(
        audio_file_path=audio_path, audio_url=url, language_code=lang
    )
    print(f"Job submitted: {result.job_id} - Status: {result.status.value}")
