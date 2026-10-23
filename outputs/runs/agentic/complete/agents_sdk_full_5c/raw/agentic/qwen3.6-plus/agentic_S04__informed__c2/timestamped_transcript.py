"""
[SAME-SCENARIO] Return word or segment timestamps from a transcription result.

Uses the AssemblyAI Transcripts API to retrieve transcriptions with
word-level and utterance-level timing information.
Provider: AssemblyAI Transcripts API
SDK: assemblyai
Auth: ASSEMBLYAI_API_KEY
"""

import sys
from typing import List, Optional, Dict, Any

from speech_client import get_assemblyai_client, poll_with_retry
from speech_models import (
    normalize_assemblyai_response,
    TranscriptResponse,
    WordSegment,
    merge_word_segments,
    split_into_sentences,
)


def get_timestamped_transcript(
    transcript_id: str,
    granularity: str = "word",
    max_retries: int = 60,
    poll_interval_seconds: int = 5,
) -> List[Dict[str, Any]]:
    """
    Retrieve a transcription result with word-level or segment-level timestamps.

    Args:
        transcript_id: The AssemblyAI transcript job ID.
        granularity: 'word' for word-level timestamps, 'segment' for sentence-level segments.
        max_retries: Maximum polling retries.
        poll_interval_seconds: Seconds between poll attempts.

    Returns:
        List of dictionaries with timestamp information.

    Raises:
        ValueError: If transcript_id is empty or granularity is invalid.
    """
    if not transcript_id:
        raise ValueError("transcript_id must not be empty")
    if granularity not in ("word", "segment"):
        raise ValueError("granularity must be 'word' or 'segment'")

    client = get_assemblyai_client()

    raw_transcript = poll_with_retry(
        client=client,
        transcript_id=transcript_id,
        max_retries=max_retries,
        poll_interval_seconds=poll_interval_seconds,
    )

    response = normalize_assemblyai_response(raw_transcript)

    if granularity == "word":
        return _extract_word_timestamps(response)
    else:
        return _extract_segment_timestamps(response)


def _extract_word_timestamps(response: TranscriptResponse) -> List[Dict[str, Any]]:
    """
    Extract word-level timestamps from a transcript response.

    Args:
        response: Normalized TranscriptResponse.

    Returns:
        List of word segments with timing, speaker, and confidence data.
    """
    results = []
    for word in response.words:
        results.append({
            "text": word.text,
            "start_ms": word.start_ms,
            "end_ms": word.end_ms,
            "confidence": word.confidence,
            "speaker": word.speaker,
        })
    return results


def _extract_segment_timestamps(response: TranscriptResponse) -> List[Dict[str, Any]]:
    """
    Extract segment-level (sentence/utterance) timestamps.

    Uses utterance boundaries from AssemblyAI output.

    Args:
        response: Normalized TranscriptResponse.

    Returns:
        List of segments with start/end timestamps and full text.
    """
    results = []

    if response.utterances:
        # Use AssemblyAI utterance boundaries
        for utterance in response.utterances:
            results.append({
                "text": utterance.text,
                "start_ms": utterance.start_ms,
                "end_ms": utterance.end_ms,
                "speaker": utterance.speaker,
                "word_count": len(utterance.words),
                "confidence": utterance.confidence,
            })
    else:
        # Fall back to splitting full text into sentences
        sentences = split_into_sentences(response.full_text)
        # Approximate timing by distributing across the audio duration
        total_words = len(response.words) if response.words else 1
        avg_ms_per_word = response.duration_ms / total_words if response.words and total_words > 0 else 0

        current_word_idx = 0
        for sentence in sentences:
            sentence_words = sentence.split()
            start_word_idx = current_word_idx
            end_word_idx = current_word_idx + len(sentence_words)

            start_ms = 0
            end_ms = 0

            if response.words and start_word_idx < len(response.words):
                start_ms = response.words[start_word_idx].start_ms
            if response.words and end_word_idx - 1 < len(response.words):
                end_ms = response.words[end_word_idx - 1].end_ms

            results.append({
                "text": sentence,
                "start_ms": start_ms,
                "end_ms": end_ms,
                "speaker": None,
                "word_count": len(sentence_words),
                "confidence": 0.0,
            })
            current_word_idx = end_word_idx

    return results


def get_words_for_time_range(
    transcript_id: str,
    start_ms: int,
    end_ms: int,
    max_retries: int = 60,
    poll_interval_seconds: int = 5,
) -> List[Dict[str, Any]]:
    """
    Get all words spoken within a specific time range.

    Args:
        transcript_id: AssemblyAI transcript job ID.
        start_ms: Start time in milliseconds.
        end_ms: End time in milliseconds.
        max_retries: Maximum polling retries.
        poll_interval_seconds: Seconds between poll attempts.

    Returns:
        List of word segments within the time range.
    """
    client = get_assemblyai_client()

    raw_transcript = poll_with_retry(
        client=client,
        transcript_id=transcript_id,
        max_retries=max_retries,
        poll_interval_seconds=poll_interval_seconds,
    )

    response = normalize_assemblyai_response(raw_transcript)

    results = []
    for word in response.words:
        if word.start_ms >= start_ms and word.end_ms <= end_ms:
            results.append({
                "text": word.text,
                "start_ms": word.start_ms,
                "end_ms": word.end_ms,
                "confidence": word.confidence,
                "speaker": word.speaker,
            })

    return results


def format_timestamped_output(
    timestamps: List[Dict[str, Any]],
    granularity: str = "word",
) -> str:
    """
    Format timestamp data as human-readable output.

    Args:
        timestamps: List of timestamped segment/word dictionaries.
        granularity: 'word' or 'segment'.

    Returns:
        Formatted string with timing information.
    """
    lines = []
    for item in timestamps:
        start_sec = item["start_ms"] / 1000.0
        end_sec = item["end_ms"] / 1000.0
        speaker_tag = f"[{item.get('speaker', '?')}]" if item.get("speaker") else ""
        confidence_str = f" ({item['confidence']:.2f})" if item.get("confidence") else ""

        if granularity == "word":
            lines.append(f"{start_sec:07.3f}-{end_sec:07.3f} {speaker_tag} {item['text']}{confidence_str}")
        else:
            lines.append(f"{start_sec:07.3f}-{end_sec:07.3f} {speaker_tag} {item['text']}")

    return "\n".join(lines)


def main():
    """CLI entry point for retrieving timestamped transcripts."""
    import argparse

    parser = argparse.ArgumentParser(description="Get timestamped transcript from AssemblyAI")
    parser.add_argument("transcript_id", help="AssemblyAI transcript job ID")
    parser.add_argument("--granularity", choices=["word", "segment"], default="word",
                        help="Granularity of timestamps")
    parser.add_argument("--format", action="store_true", help="Show human-readable output")
    parser.add_argument("--start-ms", type=int, help="Filter by start time (ms)")
    parser.add_argument("--end-ms", type=int, help="Filter by end time (ms)")

    args = parser.parse_args()

    if args.start_ms is not None and args.end_ms is not None:
        results = get_words_for_time_range(
            transcript_id=args.transcript_id,
            start_ms=args.start_ms,
            end_ms=args.end_ms,
        )
    else:
        results = get_timestamped_transcript(
            transcript_id=args.transcript_id,
            granularity=args.granularity,
        )

    if args.format:
        print(format_timestamped_output(results, args.granularity))
    else:
        import json
        print(json.dumps(results, indent=2))

    return results


if __name__ == "__main__":
    main()
