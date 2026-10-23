"""
diarized_transcript.py - Requests speaker diarization for a recorded meeting.

Submits audio to AssemblyAI with speaker_labels enabled and retrieves
the transcript with speaker identification for each utterance segment.

AssemblyAI API: https://api.assemblyai.com/v2
Model: assemblyai/nano with speaker_labels=true
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import List, Dict, Any

from speech_models import TranscriptionRequest, TranscriptionResponse, Segment
from speech_client import create_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def submit_diarized_transcription(audio_path: str) -> str:
    """
    Submit audio for transcription with speaker diarization enabled.

    Args:
        audio_path: Path to the meeting recording audio file

    Returns:
        transcription_id for polling
    """
    client = create_client()
    try:
        audio_url = client.upload_audio(audio_path)

        # AssemblyAI-specific: enable speaker_labels for diarization
        request = TranscriptionRequest(
            audio_url=audio_url,
            model="assemblyai/nano",
            speaker_labels=True,
            punctuate=True,
            format_text=True,
            language_code="en",
        )

        transcription_id = client.submit_transcription(request)
        logger.info("Diarized transcription job submitted: %s", transcription_id)
        return transcription_id
    finally:
        client.close()


def get_diarized_transcript(
    transcription_id: str,
    merge_speakers: bool = True,
) -> TranscriptionResponse:
    """
    Poll for and retrieve the diarized transcript from AssemblyAI.

    Args:
        transcription_id: The AssemblyAI job ID
        merge_speakers: Whether to merge consecutive segments from same speaker

    Returns:
        TranscriptionResponse with speaker-labeled segments
    """
    client = create_client()
    try:
        response = client.retrieve_transcription(transcription_id)
        logger.info(
            "Retrieved diarized transcript with %d utterances",
            len(response.segments),
        )
        return response
    finally:
        client.close()


def format_diarized_output(response: TranscriptionResponse) -> str:
    """Format diarized transcript for readable output."""
    lines = [
        f"Diarized Transcript (Job: {response.transcription_id})",
        f"Duration: {response.audio_duration:.2f}s",
        f"Segments: {len(response.segments)}",
        "=" * 60,
    ]

    # Track speaker changes for formatting
    prev_speaker = None
    for seg in response.segments:
        speaker = seg.speaker or "Unknown"
        if speaker != prev_speaker:
            lines.append("")
            lines.append(f"--- Speaker {speaker} ---")
            prev_speaker = speaker
        lines.append(f"  [{seg.start // 1000}s] {seg.text.strip()}")

    # Summary
    speakers = {seg.speaker for seg in response.segments if seg.speaker}
    lines.append("")
    lines.append(f"Speakers detected: {', '.join(sorted(speakers))}")

    return "\n".join(lines)


def get_speaker_summary(response: TranscriptionResponse) -> Dict[str, Dict[str, Any]]:
    """Generate per-speaker statistics from diarized transcript."""
    speaker_stats: Dict[str, Dict[str, Any]] = {}

    for seg in response.segments:
        speaker = seg.speaker or "Unknown"
        if speaker not in speaker_stats:
            speaker_stats[speaker] = {
                "segment_count": 0,
                "word_count": 0,
                "total_duration_ms": 0,
            }
        speaker_stats[speaker]["segment_count"] += 1
        speaker_stats[speaker]["word_count"] += len(seg.text.split())
        speaker_stats[speaker]["total_duration_ms"] += seg.end - seg.start

    return speaker_stats


def main():
    parser = argparse.ArgumentParser(description="Diarized transcription for meeting recordings via AssemblyAI")
    parser.add_argument("audio_file", help="Path to meeting recording audio file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--summary", action="store_true", help="Show speaker summary")
    args = parser.parse_args()

    # Submit and poll
    transcription_id = submit_diarized_transcription(args.audio_file)
    response = get_diarized_transcript(transcription_id)

    if args.json:
        print(json.dumps(response.to_dict(), indent=2))
    elif args.summary:
        stats = get_speaker_summary(response)
        print(json.dumps(stats, indent=2))
    else:
        print(format_diarized_output(response))


if __name__ == "__main__":
    main()
