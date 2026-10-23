"""
Return word or segment timestamps from a transcription result using AssemblyAI.

Retrieves detailed word-level timestamps from an AssemblyAI transcription
job that was submitted with word_timestamps enabled.
Requires ASSEMBLYAI_API_KEY environment variable.
"""

import sys
from typing import Optional, List, Dict, Any

import assemblyai
from assemblyai import AssemblyAI, Transcriber

from speech_client import get_assemblyai_client
from speech_models import (
    TranscriptionResult,
    TimestampedSegment,
    WordTimestamp,
)


def get_timestamped_transcript(
    transcript_id: str,
    api_key: Optional[str] = None,
) -> List[TimestampedSegment]:
    """
    Retrieve word-level timestamps from a completed AssemblyAI transcription.

    Fetches the transcription result and extracts word-level timing data
    that was captured when word_timestamps was enabled during submission.

    Args:
        transcript_id: AssemblyAI transcription job ID.
        api_key: Optional AssemblyAI API key override.

    Returns:
        List of TimestampedSegment objects with word-level timing.

    Raises:
        RuntimeError: If transcription failed or timestamps not available.
    """
    client = get_assemblyai_client(api_key)

    transcript = client.transcriber.get_transcript(transcript_id)

    if transcript.status == "error":
        raise RuntimeError(
            f"AssemblyAI transcription failed: {transcript.error}"
        )

    if transcript.status in ("queued", "processing"):
        raise RuntimeError(
            f"Transcription not yet complete (status: {transcript.status})"
        )

    # Convert to local model
    raw_data = transcript.dict() if hasattr(transcript, "dict") else transcript.json()
    result = TranscriptionResult.from_assemblyai_response(raw_data)

    # Check if word timestamps are available
    if not result.words:
        raise RuntimeError(
            "No word timestamps available. Ensure word_timestamps=True "
            "was set when submitting the transcription."
        )

    # Group words into segments (by utterance or sentence boundaries)
    segments = []
    if result.utterances:
        for utt in result.utterances:
            segment = TimestampedSegment.from_utterance(utt)
            segments.append(segment)
    else:
        # If no utterances, create single segment from all words
        if result.words:
            segment = TimestampedSegment(
                text=" ".join(w.text for w in result.words),
                start_ms=result.words[0].start,
                end_ms=result.words[-1].end,
                words=result.words,
            )
            segments.append(segment)

    return segments


def get_word_timestamps(
    transcript_id: str,
    api_key: Optional[str] = None,
) -> List[WordTimestamp]:
    """
    Get raw word-level timestamps from AssemblyAI transcription.

    Args:
        transcript_id: AssemblyAI transcription job ID.
        api_key: Optional AssemblyAI API key override.

    Returns:
        List of WordTimestamp objects.
    """
    client = get_assemblyai_client(api_key)

    transcript = client.transcriber.get_transcript(transcript_id)

    if transcript.status != "completed":
        raise RuntimeError(
            f"Transcription not complete (status: {transcript.status})"
        )

    raw_data = transcript.dict() if hasattr(transcript, "dict") else transcript.json()
    result = TranscriptionResult.from_assemblyai_response(raw_data)

    return result.words


def format_timestamped_segments(segments: List[TimestampedSegment]) -> str:
    """
    Format timestamped segments for display.

    Args:
        segments: List of TimestampedSegment objects.

    Returns:
        Formatted string with timestamps and text.
    """
    lines = ["Timestamped Transcript"]
    lines.append("=" * 70)

    for i, seg in enumerate(segments, 1):
        start_sec = seg.start_ms / 1000
        end_sec = seg.end_ms / 1000
        lines.append(f"\n[{start_sec:.2f}s - {end_sec:.2f}s] {seg.text}")

        # Show individual word timestamps
        for word in seg.words:
            w_start = word.start / 1000
            w_end = word.end / 1000
            lines.append(f"  {word.text} [{w_start:.3f}s-{w_end:.3f}s]")

    return "\n".join(lines)


def submit_timestamped_transcription(
    audio_url: str,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> str:
    """
    Submit audio for transcription with word timestamps enabled.

    Creates a new AssemblyAI transcription job with word_timestamps=True.

    Args:
        audio_url: URL to audio file.
        language_code: IETF language code.
        api_key: Optional AssemblyAI API key override.

    Returns:
        Transcript ID for the submitted job.
    """
    client = get_assemblyai_client(api_key)

    config = Transcriber.Config(
        audio_url=audio_url,
        language_code=language_code,
        word_timestamps=True,  # Enable AssemblyAI word-level timestamps
        punctuate=True,
        format_text=True,
    )

    transcript = client.transcriber.transcribe(config)
    return transcript.id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python timestamped_transcript.py <transcript_id>")
        sys.exit(1)

    tid = sys.argv[1]
    segments = get_timestamped_transcript(tid)
    print(format_timestamped_segments(segments))
