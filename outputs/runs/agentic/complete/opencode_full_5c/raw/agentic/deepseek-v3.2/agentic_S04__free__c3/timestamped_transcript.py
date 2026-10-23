import json
import requests
from speech_models import TimestampedWord, TimestampedSegment


def timestamped_transcript(transcript_uri: str, granularity: str = "word") -> list:
    """
    Return word or segment timestamps from a transcription result.

    Args:
        transcript_uri: URI to the transcript JSON file
        granularity: "word" for word-level timestamps or "segment" for segment-level

    Returns:
        List of timestamped words or segments
    """
    try:
        response = requests.get(transcript_uri, timeout=10)
        response.raise_for_status()
        transcript_data = response.json()

        if granularity == "word":
            return extract_word_timestamps(transcript_data)
        elif granularity == "segment":
            return extract_segment_timestamps(transcript_data)
        else:
            raise ValueError("granularity must be 'word' or 'segment'")

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch transcript from {transcript_uri}: {e}")


def extract_word_timestamps(transcript_data: dict) -> list[TimestampedWord]:
    """
    Extract word-level timestamps from AWS Transcribe transcript.
    """
    words = []

    if "items" not in transcript_data.get("results", {}):
        return words

    items = transcript_data["results"]["items"]

    for item in items:
        if item["type"] == "pronunciation":
            word = TimestampedWord(
                word=item["alternatives"][0]["content"],
                start_time=float(item["start_time"]),
                end_time=float(item["end_time"]),
                confidence=float(item["alternatives"][0].get("confidence", 0.0)),
            )
            words.append(word)

    return words


def extract_segment_timestamps(transcript_data: dict) -> list[TimestampedSegment]:
    """
    Extract segment-level timestamps from AWS Transcribe transcript.
    """
    segments = []

    if "items" not in transcript_data.get("results", {}):
        return segments

    items = transcript_data["results"]["items"]
    current_segment = []
    segment_start = None
    segment_end = None

    for item in items:
        if item["type"] == "pronunciation":
            if segment_start is None:
                segment_start = float(item["start_time"])

            current_segment.append(item["alternatives"][0]["content"])
            segment_end = float(item["end_time"])

        elif item["type"] == "punctuation" and item["alternatives"][0]["content"] in [
            ".",
            "!",
            "?",
        ]:
            if current_segment:
                segments.append(
                    TimestampedSegment(
                        text=" ".join(current_segment)
                        + item["alternatives"][0]["content"],
                        start_time=segment_start,
                        end_time=segment_end,
                        word_count=len(current_segment),
                    )
                )
                current_segment = []
                segment_start = None
                segment_end = None

    if current_segment:
        segments.append(
            TimestampedSegment(
                text=" ".join(current_segment),
                start_time=segment_start,
                end_time=segment_end,
                word_count=len(current_segment),
            )
        )

    return segments
