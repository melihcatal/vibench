import os
from typing import Optional

from speech_client import load_config, transcribe_client
from speech_models import TranscriptionRequest, build_transcribe_kwargs


def submit_transcription(audio_uri: str, job_name: Optional[str] = None) -> dict:
    config = load_config()
    client = transcribe_client(config.region_name)
    request = TranscriptionRequest(
        job_name=job_name or os.getenv('AWS_TRANSCRIBE_JOB_NAME', 'batch-speech-to-text-job'),
        media_uri=audio_uri,
        media_format=config.media_format,
        language_code=config.language_code,
        output_bucket=config.output_bucket,
        vocabulary_name=config.vocabulary_name,
        terminology_name=config.terminology_name,
    )
    kwargs = build_transcribe_kwargs(request)
    return client.start_transcription_job(**kwargs)
