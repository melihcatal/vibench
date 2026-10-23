"""
Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text API
SDK: google-cloud-speech
Endpoint: speech.googleapis.com
Feature: enable_word_time_offsets for word-level timing
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptSegment,
    TimestampedSegment,
    WordTimestamp,
    normalize_google_results_to_segments,
    build_timestamped_segments,
)


def extract_word_timestamps(
    segments: List[TranscriptSegment],
) -> List[TimestampedSegment]:
    """
    Extract word-level timestamps from transcription segments.

    Requires that the original transcription was submitted with
    enable_word_time_offsets=True.

    Args:
        segments: List of TranscriptSegment with word timing data.

    Returns:
        List of TimestampedSegment with computed start/end times.
    """
    return build_timestamped_segments(segments)


def get_segment_timing(segment: TranscriptSegment) -> Dict[str, Any]:
    """
    Get timing information for a single transcript segment.
    """
    if not segment.words:
        return {
            "transcript": segment.transcript,
            "has_timestamps": False,
        }

    return {
        "transcript": segment.transcript,
        "has_timestamps": True,
        "start_time_seconds": segment.words[0].start_offset_seconds,
        "end_time_seconds": segment.words[-1].end_offset_seconds,
        "duration_seconds": round(
            segment.words[-1].end_offset_seconds - segment.words[0].start_offset_seconds, 3
        ),
        "word_count": len(segment.words),
        "confidence": segment.confidence,
    }


def format_timestamped_text(timestamped: List[TimestampedSegment]) -> str:
    """
    Format timestamped segments with timing markers.
    """
    lines = []
    for ts in timestamped:
        start = f"[{ts.start_time_seconds:.2f}s]"
        end = f"[{ts.end_time_seconds:.2f}s]"
        lines.append(f"{start} -> {end} {ts.transcript}")
    return "\n".join(lines)


def get_word_level_timeline(
    timestamped: List[TimestampedSegment],
) -> List[Dict[str, Any]]:
    """
    Build a complete word-level timeline across all segments.
    """
    timeline = []
    for ts in timestamped:
        for word_ts in ts.words:
            timeline.append({
                "segment_id": ts.segment_id,
                "word": word_ts.word,
                "start_offset_seconds": round(word_ts.start_offset_seconds, 3),
                "end_offset_seconds": round(word_ts.end_offset_seconds, 3),
                "speaker_tag": word_ts.speaker_tag,
                "confidence": word_ts.confidence,
            })
    return timeline


def search_by_timestamp(
    timestamped: List[TimestampedSegment],
    target_seconds: float,
    tolerance: float = 1.0,
) -> Optional[Dict[str, Any]]:
    """
    Find the segment containing a specific timestamp.

    Args:
        timestamped: List of TimestampedSegment
        target_seconds: Target time in seconds
        tolerance: Acceptable time window in seconds

    Returns:
        Matching segment info or None.
    """
    for ts in timestamped:
        if abs(ts.start_time_seconds - target_seconds) <= tolerance:
            return {
                "segment_id": ts.segment_id,
                "transcript": ts.transcript,
                "start_time_seconds": ts.start_time_seconds,
                "end_time_seconds": ts.end_time_seconds,
            }
    return None


def export_srt_format(timestamped: List[TimestampedSegment]) -> str:
    """
    Export timestamped segments in SRT subtitle format.

    SRT format is compatible with video players and subtitle editors.
    """
    lines = []
    for idx, ts in enumerate(timestamped, 1):
        start = format_srt_time(ts.start_time_seconds)
        end = format_srt_time(ts.end_time_seconds)
        lines.append(f"{idx}")
        lines.append(f"{start} --> {end}")
        lines.append(ts.transcript)
        lines.append("")
    return "\n".join(lines)


def format_srt_time(seconds: float) -> str:
    """
    Format seconds as SRT timestamp (HH:MM:SS,mmm).
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


if __name__ == "__main__":
    import sys

    print("Usage: Import timestamped_transcript and use with transcription results.")
    print("Example:")
    print("  from timestamped_transcript import extract_word_timestamps")
    print("  from poll_transcription import poll_and_parse_transcript")
    print("  result = poll_and_parse_transcript(operation_name)")
    print("  timestamped = extract_word_timestamps(result.results)")
