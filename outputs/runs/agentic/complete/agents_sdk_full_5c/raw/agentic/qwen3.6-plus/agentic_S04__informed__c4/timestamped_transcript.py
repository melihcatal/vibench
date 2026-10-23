"""Return word or segment timestamps from a transcription result using AssemblyAI Transcripts API.

Uses the AssemblyAI Python SDK (assemblyai) to retrieve timestamp data from a completed transcription.
Auth: ASSEMBLYAI_API_KEY environment variable.
"""

import sys
from typing import List, Optional

from assemblyai import Transcriber

from speech_models import TranscriptionResponse, Word, normalize_assemblyai_response


def get_timestamped_transcript(
    job_id: str,
    granularity: str = "word",
) -> TranscriptionResponse:
    """Fetch a completed transcription with word-level timestamps from AssemblyAI.

    Args:
        job_id: The AssemblyAI transcription job ID.
        granularity: 'word' for word-level timestamps, 'segment' for segment-level.

    Returns:
        TranscriptionResponse populated with words and their start/end timestamps.
    """
    transcriber = Transcriber()
    transcript = transcriber.get_transcript_by_id(job_id)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    if transcript.status != "completed":
        raise RuntimeError(
            f"Transcription not yet complete. Current status: {transcript.status}"
        )

    return normalize_assemblyai_response(transcript)


def format_word_timestamps(response: TranscriptionResponse) -> List[dict]:
    """Format word-level timestamps as a list of dicts."""
    return [
        {
            "text": w.text,
            "start_ms": w.start_ms,
            "end_ms": w.end_ms,
            "confidence": w.confidence,
        }
        for w in response.words
    ]


def format_segment_timestamps(response: TranscriptionResponse) -> List[dict]:
    """Format segment-level timestamps as a list of dicts."""
    segments = []
    for seg in response.segments:
        segments.append({
            "text": seg.text,
            "start_ms": seg.start_ms,
            "end_ms": seg.end_ms,
            "speaker": seg.speaker,
            "confidence": seg.confidence,
        })
    if not segments:
        segments.append({
            "text": response.transcript,
            "start_ms": None,
            "end_ms": None,
            "speaker": None,
            "confidence": 0.0,
        })
    return segments


def main():
    job_id = sys.argv[1] if len(sys.argv) > 1 else None
    granularity = sys.argv[2] if len(sys.argv) > 2 else "word"

    if not job_id:
        print("Usage: python timestamped_transcript.py <job_id> [word|segment]")
        sys.exit(1)

    result = get_timestamped_transcript(job_id, granularity=granularity)

    if granularity == "word":
        timestamps = format_word_timestamps(result)
        print(f"Word-level timestamps for job {result.job_id}:")
        for entry in timestamps:
            print(f"  [{entry['start_ms']}ms - {entry['end_ms']}ms] {entry['text']}")
    else:
        timestamps = format_segment_timestamps(result)
        print(f"Segment-level timestamps for job {result.job_id}:")
        for entry in timestamps:
            print(f"  [{entry['start_ms']}ms - {entry['end_ms']}ms] {entry['text']}")


if __name__ == "__main__":
    main()
