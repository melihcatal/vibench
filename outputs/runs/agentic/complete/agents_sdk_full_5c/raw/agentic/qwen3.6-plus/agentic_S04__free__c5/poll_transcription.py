"""
Poll a transcription job and return the transcript using AWS Transcribe.

Provider: AWS Transcribe (amazon.transcribe)
SDK: boto3
Endpoint: transcribe.{region}.amazonaws.com
"""

import json
import time
from typing import Optional

import boto3

from speech_client import get_transcribe_client, parse_s3_uri
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    normalize_aws_transcribe_response,
)


def get_transcription_job_status(job_name: str) -> dict:
    """
    Get the current status of an AWS Transcribe job.

    Args:
        job_name: Name of the transcription job

    Returns:
        dict with job_name, status, and optional output_uri
    """
    client = get_transcribe_client()
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response.get("TranscriptionJob", {})

    result = {
        "job_name": job.get("TranscriptionJobName"),
        "status": job.get("TranscriptionJobStatus"),
        "language_code": job.get("LanguageCode"),
    }

    if job.get("Transcript", {}).get("TranscriptFileUri"):
        result["output_uri"] = job["Transcript"]["TranscriptFileUri"]

    if job.get("FailureReason"):
        result["failure_reason"] = job["FailureReason"]

    return result


def poll_transcription_job(
    job_name: str,
    interval_seconds: int = 10,
    max_wait_seconds: int = 3600,
) -> TranscriptionResult:
    """
    Poll an AWS Transcribe job until completion or timeout.

    Args:
        job_name: Name of the transcription job to poll
        interval_seconds: Seconds between poll attempts
        max_wait_seconds: Maximum total wait time before timeout

    Returns:
        TranscriptionResult with full transcript and segments

    Raises:
        TimeoutError: If job does not complete within max_wait_seconds
        RuntimeError: If transcription job fails
    """
    client = get_transcribe_client()
    elapsed = 0

    while elapsed < max_wait_seconds:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        job = response.get("TranscriptionJob", {})
        status_str = job.get("TranscriptionJobStatus")

        if status_str == TranscriptionStatus.COMPLETED.value:
            transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
            transcription_output = _fetch_transcription_output(transcript_uri, client)
            return normalize_aws_transcribe_response(
                job_name=job_name,
                get_job_response=response,
                transcription_output=transcription_output,
            )

        if status_str == TranscriptionStatus.FAILED.value:
            failure_reason = job.get("FailureReason", "Unknown failure")
            result = normalize_aws_transcribe_response(job_name, response)
            result.failure_reason = failure_reason
            raise RuntimeError(f"Transcription job failed: {failure_reason}")

        if status_str in (TranscriptionStatus.QUEUED.value, TranscriptionStatus.IN_PROGRESS.value):
            time.sleep(interval_seconds)
            elapsed += interval_seconds
        else:
            raise RuntimeError(f"Unexpected job status: {status_str}")

    raise TimeoutError(
        f"Transcription job '{job_name}' did not complete within {max_wait_seconds} seconds"
    )


def poll_once(job_name: str) -> dict:
    """
    Poll an AWS Transcribe job once without waiting.

    Args:
        job_name: Name of the transcription job

    Returns:
        dict with job_name, status, and optional transcript text
    """
    client = get_transcribe_client()
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response.get("TranscriptionJob", {})
    status_str = job.get("TranscriptionJobStatus")

    result = {
        "job_name": job_name,
        "status": status_str,
    }

    if status_str == TranscriptionStatus.COMPLETED.value:
        transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
        transcription_output = _fetch_transcription_output(transcript_uri, client)
        normalized = normalize_aws_transcribe_response(
            job_name=job_name,
            get_job_response=response,
            transcription_output=transcription_output,
        )
        result["transcript"] = normalized.transcript_text
        result["segments"] = [
            {
                "segment_id": s.segment_id,
                "speaker": s.speaker,
                "text": s.text,
                "start_time_ms": s.start_time_ms,
                "end_time_ms": s.end_time_ms,
            }
            for s in normalized.segments
        ]
    elif status_str == TranscriptionStatus.FAILED.value:
        result["failure_reason"] = job.get("FailureReason")

    return result


def _fetch_transcription_output(
    transcript_uri: Optional[str],
    client: boto3.client,
) -> Optional[dict]:
    """Fetch the transcription output JSON from S3 using the AWS Transcribe client session."""
    if not transcript_uri:
        return None

    bucket, key = parse_s3_uri(transcript_uri)
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return json.loads(response["Body"].read().decode("utf-8"))
