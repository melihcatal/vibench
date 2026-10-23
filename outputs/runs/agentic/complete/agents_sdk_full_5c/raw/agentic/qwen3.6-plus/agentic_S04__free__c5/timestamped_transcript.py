"""
Return word or segment timestamps from a transcription result using AWS Transcribe.

Provider: AWS Transcribe (amazon.transcribe)
SDK: boto3
Endpoint: transcribe.{region}.amazonaws.com
Feature: Word-level timestamps and ShowWordConfidence
"""

import json
from typing import Optional

from speech_client import get_transcribe_client, parse_s3_uri
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    WordTiming,
    Segment,
    normalize_aws_transcribe_response,
)


def get_timestamped_transcript(
    job_name: str,
    granularity: str = "word",
) -> list[dict]:
    """
    Return word-level or segment-level timestamps from an AWS Transcribe result.

    Args:
        job_name: Name of the completed transcription job
        granularity: 'word' for word-level timestamps, 'segment' for phrase segments

    Returns:
        list of timestamp entries with word/segment text and timing info
    """
    client = get_transcribe_client()
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response.get("TranscriptionJob", {})
    status = job.get("TranscriptionJobStatus")

    if status != TranscriptionStatus.COMPLETED.value:
        raise ValueError(f"Job is not complete. Status: {status}")

    transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
    if not transcript_uri:
        raise ValueError("No transcript URI available")

    bucket, key = parse_s3_uri(transcript_uri)
    s3_client = boto3.client("s3")
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    transcription_data = json.loads(obj["Body"].read().decode("utf-8"))

    if granularity == "word":
        return _extract_word_timestamps(transcription_data)
    elif granularity == "segment":
        return _extract_segment_timestamps(transcription_data)
    else:
        raise ValueError(f"Unknown granularity: {granularity}. Use 'word' or 'segment'.")


def _extract_word_timestamps(data: dict) -> list[dict]:
    """Extract word-level timestamps from AWS Transcribe JSON output."""
    results = data.get("results", {})
    items = results.get("items", [])

    word_timestamps = []
    for item in items:
        if item.get("type") != "pronunciation":
            continue

        alternatives = item.get("alternatives", [{}])
        word_content = alternatives[0].get("content", "")
        confidence = float(alternatives[0].get("confidence", 0))
        start_time = float(item.get("start_time", 0))
        end_time = float(item.get("end_time", 0))
        speaker = item.get("speaker_label")

        entry = {
            "word": word_content,
            "start_time_ms": round(start_time * 1000, 2),
            "end_time_ms": round(end_time * 1000, 2),
            "duration_ms": round((end_time - start_time) * 1000, 2),
            "confidence": round(confidence, 4),
        }
        if speaker:
            entry["speaker"] = speaker

        word_timestamps.append(entry)

    return word_timestamps


def _extract_segment_timestamps(data: dict) -> list[dict]:
    """Extract segment-level timestamps from AWS Transcribe JSON output."""
    results = data.get("results", {})
    items = results.get("items", [])

    segments = []
    current_segment_words = []
    current_start = None
    current_end = None

    for item in items:
        if item.get("type") == "punctuation":
            if current_segment_words:
                current_segment_words[-1]["word"] += item.get("value", "")
            continue

        if item.get("type") == "pronunciation":
            start_time = float(item.get("start_time", 0))
            end_time = float(item.get("end_time", 0))
            word = item.get("alternatives", [{}])[0].get("content", "")
            confidence = float(item.get("alternatives", [{}])[0].get("confidence", 0))
            speaker = item.get("speaker_label")

            if current_start is None:
                current_start = start_time

            current_end = end_time
            current_segment_words.append({
                "word": word,
                "start_time_ms": round(start_time * 1000, 2),
                "end_time_ms": round(end_time * 1000, 2),
                "confidence": round(confidence, 4),
                "speaker": speaker,
            })

            if len(current_segment_words) >= 20:
                segments.append(_build_segment(current_segment_words, current_start, current_end))
                current_segment_words = []
                current_start = None
                current_end = None

    if current_segment_words:
        segments.append(_build_segment(current_segment_words, current_start, current_end))

    return segments


def _build_segment(
    words: list[dict],
    start_time: Optional[float],
    end_time: Optional[float],
) -> dict:
    """Build a segment dict from word-level data."""
    text = " ".join(w["word"] for w in words)
    avg_confidence = sum(w["confidence"] for w in words) / len(words) if words else 0

    return {
        "text": text,
        "start_time_ms": round((start_time or 0) * 1000, 2),
        "end_time_ms": round((end_time or 0) * 1000, 2),
        "word_count": len(words),
        "avg_confidence": round(avg_confidence, 4),
        "words": words,
    }


def get_word_confidence_report(job_name: str) -> dict:
    """
    Generate a confidence report for word-level timestamps in a transcription.

    Args:
        job_name: Name of the transcription job

    Returns:
        dict with confidence statistics
    """
    word_timestamps = get_timestamped_transcript(job_name, granularity="word")

    if not word_timestamps:
        return {"total_words": 0, "avg_confidence": 0}

    confidences = [w["confidence"] for w in word_timestamps]
    low_confidence_words = [w for w in word_timestamps if w["confidence"] < 0.7]

    return {
        "total_words": len(word_timestamps),
        "avg_confidence": round(sum(confidences) / len(confidences), 4),
        "min_confidence": round(min(confidences), 4),
        "max_confidence": round(max(confidences), 4),
        "low_confidence_count": len(low_confidence_words),
        "low_confidence_words": low_confidence_words[:50],
    }
