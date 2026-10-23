"""
timestamped_transcript.py - Returns word or segment timestamps from a transcription result.

Retrieves detailed word-level timestamps from an AssemblyAI transcription job,
providing start/end times in milliseconds for each word and segment.

AssemblyAI API: https://api.assemblyai.com/v2/transcript/{id}
Returns words array with start, end, and confidence for each word.
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import List, Dict, Any, Optional

from speech_models import (
    TranscriptionResponse,
    TranscriptionStatus,
    WordTimestamp,
    Segment,
)
from speech_client import create_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def get_timestamped_transcript(
    transcription_id: str,
) -> TranscriptionResponse:
    """
    Retrieve a transcription result with word-level timestamps from AssemblyAI.

    Args:
        transcription_id: The AssemblyAI transcription job ID

    Returns:
        TranscriptionResponse with word timestamps populated
    """
    client = create_client()
    try:
        response = client.retrieve_transcription(transcription_id)
        logger.info(
            "Retrieved timestamped transcript with %d words",
            len(response.words),
        )
        return response
    finally:
        client.close()


def get_segment_timestamps(
    transcription_id: str,
) -> List[Segment]:
    """
    Retrieve segment-level timestamps from AssemblyAI transcription.

    Returns segments with start/end times for each utterance.
    """
    client = create_client()
    try:
        response = client.retrieve_transcription(transcription_id)
        return response.segments
    finally:
        client.close()


def get_word_timestamps(
    transcription_id: str,
) -> List[WordTimestamp]:
    """
    Retrieve word-level timestamps from AssemblyAI transcription.

    Returns individual words with precise start/end millisecond offsets.
    """
    client = create_client()
    try:
        response = client.retrieve_transcription(transcription_id)
        return response.words
    finally:
        client.close()


def format_timestamped_output(response: TranscriptionResponse) -> str:
    """Format timestamped transcript for readable output."""
    lines = [
        f"Timestamped Transcript (Job: {response.transcription_id})",
        f"Duration: {response.audio_duration:.2f}s",
        f"Words: {len(response.words)}",
        "=" * 80,
    ]

    # Word-level timestamps
    lines.append("WORD-LEVEL TIMESTAMPS:")
    for i, word in enumerate(response.words):
        lines.append(
            f"  [{word.start:06d}ms - {word.end:06d}] ({word.confidence:.2f}) {word.text}"
        )

    # Segment-level timestamps
    if response.segments:
        lines.append("")
        lines.append("SEGMENT-LEVEL TIMESTAMPS:")
        for seg in response.segments:
            speaker = f"[Speaker {seg.speaker}] " if seg.speaker else ""
            lines.append(
                f"  [{seg.start // 1000:03d}s - {seg.end // 1000:03d}s] "
                f"{speaker}{seg.text.strip()}"
            )

    return "\n".join(lines)


def export_srt(
    transcription_id: str,
    output_path: Optional[str] = None,
) -> str:
    """
    Export transcription as SRT subtitle format using AssemblyAI word timestamps.
    
    AssemblyAI provides millisecond precision which maps directly to SRT format.
    """
    words = get_word_timestamps(transcription_id)

    # Group words into segments of ~15 words or 3 seconds
    srt_entries = []
    current_words = []
    current_start = None
    current_end = None
    max_duration_ms = 3000
    max_words = 15

    for word in words:
        if current_start is None:
            current_start = word.start
            current_end = word.end
            current_words.append(word)
        elif (word.end - current_start) > max_duration_ms or len(current_words) >= max_words:
            # Write current segment
            text = " ".join(w.text for w in current_words)
            srt_entries.append({
                "start": current_start,
                "end": current_end,
                "text": text,
            })
            current_start = word.start
            current_end = word.end
            current_words = [word]
        else:
            current_words.append(word)
            current_end = word.end

    # Flush remaining
    if current_words:
        text = " ".join(w.text for w in current_words)
        srt_entries.append({
            "start": current_start,
            "end": current_end,
            "text": text,
        })

    # Format as SRT
    def format_srt_time(ms: int) -> str:
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        millis = ms % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

    srt_content = []
    for i, entry in enumerate(srt_entries, 1):
        srt_content.append(str(i))
        srt_content.append(f"{format_srt_time(entry['start'])} --> {format_srt_time(entry['end'])}")
        srt_content.append(entry["text"])
        srt_content.append("")

    result = "\n".join(srt_content)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        logger.info("SRT exported to: %s", output_path)

    return result


def main():
    parser = argparse.ArgumentParser(description="Get word/segment timestamps from AssemblyAI transcription")
    parser.add_argument("transcription_id", help="AssemblyAI transcription job ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--srt", help="Export as SRT file to given path")
    args = parser.parse_args()

    response = get_timestamped_transcript(args.transcription_id)

    if args.json:
        print(json.dumps(response.to_dict(), indent=2))
    elif args.srt:
        srt = export_srt(args.transcription_id, args.srt)
        print(f"SRT exported to {args.srt}")
    else:
        print(format_timestamped_output(response))


if __name__ == "__main__":
    main()
