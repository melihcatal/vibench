"""
Request speaker diarization for a recorded meeting using AWS Transcribe.

Provider: AWS Transcribe (amazon.transcribe)
SDK: boto3
Endpoint: transcribe.{region}.amazonaws.com
Feature: Speaker Labels (ShowSpeakerLabels, MaxSpeakerLabels)
"""

import json
import uuid
from typing import Optional

from speech_client import (
    get_transcribe_client,
    parse_s3_uri,
    AWS_DEFAULT_BUCKET,
    build_s3_uri,
)
from speech_models import (
    TranscriptionRequest,
    LanguageCode,
    TranscriptionResult,
    TranscriptionStatus,
    normalize_aws_transcribe_response,
    Segment,
    WordTiming,
)


def submit_diarized_transcription(
    audio_uri: str,
    max_speakers: int = 4,
    job_name: Optional[str] = None,
    language_code: LanguageCode = LanguageCode.EN_US,
    output_bucket: Optional[str] = None,
) -> dict:
    """
    Submit an audio file for batch transcription with speaker diarization enabled.

    Uses AWS Transcribe's Speaker Labels feature to identify different speakers.

    Args:
        audio_uri: S3 URI of the audio recording
        max_speakers: Maximum number of speakers to identify (2-10)
        job_name: Optional job name
        language_code: Language code for the audio
        output_bucket: S3 bucket for output

    Returns:
        dict with job_name and status
    """
    client = get_transcribe_client()

    if not job_name:
        job_name = f"diarized-meeting-{uuid.uuid4().hex[:12]}"

    output_bucket = output_bucket or AWS_DEFAULT_BUCKET

    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_uri},
        LanguageCode=language_code.value,
        OutputBucketName=output_bucket,
        OutputKey=f"diarized/{job_name}.json",
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": max_speakers,
        },
    )

    job = response.get("TranscriptionJob", {})
    return {
        "job_name": job.get("TranscriptionJobName"),
        "status": job.get("TranscriptionJobStatus"),
        "speaker_labels_enabled": True,
        "max_speakers": max_speakers,
    }


def get_diarized_transcript(
    job_name: str,
    poll: bool = False,
    max_wait_seconds: int = 3600,
) -> list[dict]:
    """
    Retrieve a diarized transcript with speaker identification from AWS Transcribe.

    Args:
        job_name: Name of the completed transcription job
        poll: If True, poll until completion
        max_wait_seconds: Maximum wait time if polling

    Returns:
        list of dicts with speaker, text, start_time, end_time
    """
    import time
    from poll_transcription import poll_once

    client = get_transcribe_client()

    if poll:
        elapsed = 0
        interval = 15
        while elapsed < max_wait_seconds:
            status = poll_once(job_name)
            if status["status"] == "COMPLETED":
                break
            elif status["status"] == "FAILED":
                raise RuntimeError(f"Job failed: {status.get('failure_reason')}")
            time.sleep(interval)
            elapsed += interval
        else:
            raise TimeoutError(f"Job {job_name} did not complete in time")
    else:
        status = poll_once(job_name)
        if status["status"] != "COMPLETED":
            raise ValueError(f"Job is not complete. Current status: {status['status']}")

    response = client.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    bucket, key = parse_s3_uri(transcript_uri)

    s3_client = boto3.client("s3")
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    transcription_data = json.loads(obj["Body"].read().decode("utf-8"))

    return _parse_diarized_segments(transcription_data)


def _parse_diarized_segments(data: dict) -> list[dict]:
    """Parse AWS Transcribe output with speaker labels into diarized segments."""
    results = data.get("results", {})
    speaker_segments = results.get("speaker_labels", {}).get("segments", [])
    items = results.get("items", [])

    speaker_items_map = _build_speaker_map(speaker_segments, items)
    diarized_segments = []

    for segment in speaker_segments:
        speaker_label = f"speaker_{segment.get('speaker_label', 'unknown')}"
        start_time = float(segment.get("start_time", 0))
        end_time = float(segment.get("end_time", 0))

        words = []
        for item in segment.get("items", []):
            speaker = item.get("speaker_label")
            if speaker:
                words.append(f"speaker_{speaker}")

        segment_words = speaker_items_map.get(
            (start_time, end_time), []
        )
        text = " ".join(w["word"] for w in segment_words) if segment_words else ""

        diarized_segments.append({
            "speaker": speaker_label,
            "text": text,
            "start_time_ms": start_time * 1000,
            "end_time_ms": end_time * 1000,
            "word_count": len(segment_words),
        })

    return diarized_segments


def _build_speaker_map(
    speaker_segments: list[dict],
    items: list[dict],
) -> dict:
    """Build a mapping of time ranges to speaker-labeled items."""
    speaker_map = {}
    for item in items:
        if item.get("type") == "punctuation":
            continue
        start = float(item.get("start_time", 0))
        end = float(item.get("end_time", 0))
        word = item.get("alternatives", [{}])[0].get("content", "")
        speaker = item.get("speaker_label")

        key = (start, end)
        if key not in speaker_map:
            speaker_map[key] = []
        speaker_map[key].append({
            "word": word,
            "speaker": speaker,
            "start_time": start,
            "end_time": end,
        })

    return speaker_map


def request_meeting_diarization(
    meeting_audio_uri: str,
    expected_speakers: int = 4,
    language_code: LanguageCode = LanguageCode.EN_US,
) -> dict:
    """
    High-level function to request speaker diarization for a recorded meeting.

    Args:
        meeting_audio_uri: S3 URI of the meeting recording
        expected_speakers: Expected number of meeting participants
        language_code: Language of the meeting

    Returns:
        dict with submission details
    """
    return submit_diarized_transcription(
        audio_uri=meeting_audio_uri,
        max_speakers=expected_speakers,
        language_code=language_code,
    )
