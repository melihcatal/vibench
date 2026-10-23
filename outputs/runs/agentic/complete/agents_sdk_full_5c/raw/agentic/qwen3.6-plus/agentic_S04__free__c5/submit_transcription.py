"""
Submit an audio file for batch transcription using AWS Transcribe.

Provider: AWS Transcribe (amazon.transcribe)
SDK: boto3
Endpoint: transcribe.{region}.amazonaws.com
"""

import uuid
from typing import Optional

from speech_client import (
    get_transcribe_client,
    AWS_DEFAULT_BUCKET,
    build_s3_uri,
)
from speech_models import (
    TranscriptionRequest,
    LanguageCode,
)


def submit_transcription_job(
    audio_uri: str,
    job_name: Optional[str] = None,
    language_code: LanguageCode = LanguageCode.EN_US,
    output_bucket: Optional[str] = None,
    output_prefix: Optional[str] = "transcription-output",
    enable_word_timestamps: bool = True,
    vocabulary_name: Optional[str] = None,
    tags: Optional[list[dict[str, str]]] = None,
) -> dict:
    """
    Submit an audio file for batch transcription to AWS Transcribe.

    Args:
        audio_uri: S3 URI of the audio file (e.g., s3://bucket/key)
        job_name: Optional job name; generated if not provided
        language_code: Language code for the audio
        output_bucket: S3 bucket for transcription results
        output_prefix: Key prefix for output JSON
        enable_word_timestamps: Request word-level timestamps
        vocabulary_name: Optional custom vocabulary name
        tags: Optional tags for the transcription job

    Returns:
        dict with job_name, status, and media_file_uri
    """
    client = get_transcribe_client()

    if not job_name:
        job_name = f"batch-transcribe-{uuid.uuid4().hex[:12]}"

    output_bucket = output_bucket or AWS_DEFAULT_BUCKET

    settings = {}
    if enable_word_timestamps:
        settings["ShowWordConfidence"] = True

    request_kwargs = {
        "TranscriptionJobName": job_name,
        "Media": {"MediaFileUri": audio_uri},
        "LanguageCode": language_code.value,
        "OutputBucketName": output_bucket,
        "OutputKey": f"{output_prefix}/{job_name}.json",
        "Settings": settings,
    }

    if vocabulary_name:
        request_kwargs["Settings"]["VocabularyName"] = vocabulary_name

    if tags:
        request_kwargs["Tags"] = tags

    response = client.start_transcription_job(**request_kwargs)

    job_status = response.get("TranscriptionJob", {})
    return {
        "job_name": job_status.get("TranscriptionJobName", job_name),
        "status": job_status.get("TranscriptionJobStatus", "IN_PROGRESS"),
        "media_file_uri": audio_uri,
        "output_uri": build_s3_uri(output_bucket, f"{output_prefix}/{job_name}.json"),
        "language_code": language_code.value,
    }


def submit_from_request(request: TranscriptionRequest) -> dict:
    """
    Submit a batch transcription job from a TranscriptionRequest object.

    Args:
        request: Normalized TranscriptionRequest

    Returns:
        dict with job details
    """
    settings = {}
    if request.enable_word_timestamps:
        settings["ShowWordConfidence"] = True

    if request.enable_diarization:
        settings["ShowSpeakerLabels"] = True
        if request.max_speaker_labels:
            settings["MaxSpeakerLabels"] = request.max_speaker_labels

    if request.vocabulary_name:
        settings["VocabularyName"] = request.vocabulary_name

    request_kwargs = {
        "TranscriptionJobName": request.job_name,
        "Media": {"MediaFileUri": request.media_uri},
        "LanguageCode": request.language_code.value,
        "OutputBucketName": request.output_bucket_name or AWS_DEFAULT_BUCKET,
        "Settings": settings,
    }

    if request.output_key_prefix:
        request_kwargs["OutputKey"] = f"{request.output_key_prefix}/{request.job_name}.json"

    if request.channel_id is not None:
        request_kwargs["ChannelId"] = request.channel_id

    if request.tags:
        request_kwargs["Tags"] = request.tags

    client = get_transcribe_client()
    response = client.start_transcription_job(**request_kwargs)

    job = response.get("TranscriptionJob", {})
    return {
        "job_name": job.get("TranscriptionJobName"),
        "status": job.get("TranscriptionJobStatus"),
        "media_uri": job.get("Media", {}).get("MediaFileUri"),
        "output_location": job.get("OutputLocation"),
    }
