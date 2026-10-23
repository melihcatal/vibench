import os
from openai import OpenAI
from speech_client import get_openai_client, OPENAI_WHISPER_MODEL
from speech_models import TranscriptionJob, TranscriptionStatus


def submit_transcription(
    audio_file_path: str, language: str | None = None, model: str = OPENAI_WHISPER_MODEL
) -> TranscriptionJob:
    client: OpenAI = get_openai_client()
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=model,
            language=language,
            response_format="verbose_json",
            temperature=0.0,
        )
    job_id = getattr(transcription, "id", os.urandom(16).hex())
    return TranscriptionJob(
        job_id=job_id,
        status=TranscriptionStatus.COMPLETED,
        audio_url=audio_file_path,
        error=None,
    )


def submit_batch_transcription(
    audio_file_path: str, language: str | None = None, model: str = OPENAI_WHISPER_MODEL
) -> TranscriptionJob:
    client: OpenAI = get_openai_client()
    with open(audio_file_path, "rb") as audio_file:
        file_obj = client.files.create(file=audio_file, purpose="transcriptions")
    batch_input = {
        "custom_id": "transcription_001",
        "method": "POST",
        "url": "/v1/audio/transcriptions",
        "body": {
            "model": model,
            "file": file_obj.id,
            "language": language,
            "response_format": "verbose_json",
        },
    }
    batch_file = client.files.create(
        file=iter([str(batch_input).encode("utf-8")]),
        purpose="batch",
    )
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/audio/transcriptions",
        completion_window="24h",
    )
    return TranscriptionJob(
        job_id=batch_job.id,
        status=TranscriptionStatus.QUEUED,
        audio_url=audio_file_path,
        error=None,
    )
