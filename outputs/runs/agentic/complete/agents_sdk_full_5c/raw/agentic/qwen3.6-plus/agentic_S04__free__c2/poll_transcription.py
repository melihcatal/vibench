"""
poll_transcription.py - Polls a transcription job and returns the transcript.

Polls AssemblyAI's transcription API until the job is complete, then returns
the full transcript text. Handles status checking and error conditions.

AssemblyAI API: https://api.assemblyai.com/v2/transcript/{id}
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from speech_models import TranscriptionResponse, TranscriptionStatus
from speech_client import create_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def poll_transcription_job(
    transcription_id: str,
    poll_interval: int = 5,
    max_polls: int = 120,
) -> TranscriptionResponse:
    """
    Poll an AssemblyAI transcription job until completion and return the result.

    Args:
        transcription_id: The AssemblyAI transcription job ID
        poll_interval: Seconds between polls
        max_polls: Maximum number of poll attempts

    Returns:
        TranscriptionResponse with the completed transcript

    Raises:
        RuntimeError: If transcription fails
        TimeoutError: If polling exceeds max attempts
    """
    client = create_client()
    client.config.poll_interval = poll_interval
    client.config.max_polls = max_polls

    try:
        result = client.retrieve_transcription(transcription_id)
        logger.info(
            "Transcription %s completed with status: %s",
            transcription_id,
            result.status,
        )
        return result
    finally:
        client.close()


def format_transcript_output(response: TranscriptionResponse) -> str:
    """Format the transcript for display."""
    if response.status == TranscriptionStatus.ERROR:
        return f"ERROR: {response.error}"

    lines = [
        f"Transcription ID: {response.transcription_id}",
        f"Status: {response.status.value}",
        f"Audio Duration: {response.audio_duration:.2f}s",
        f"Confidence: {response.confidence:.2%}",
        "",
        "TRANSCRIPT:",
        response.text,
    ]

    if response.segments:
        lines.append("")
        lines.append("SEGMENTS:")
        for i, seg in enumerate(response.segments):
            speaker_label = f"[Speaker {seg.speaker}]" if seg.speaker else ""
            lines.append(f"  {speaker_label} {seg.text.strip()}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Poll AssemblyAI transcription job")
    parser.add_argument("transcription_id", help="AssemblyAI transcription job ID")
    parser.add_argument("--interval", type=int, default=5, help="Poll interval in seconds")
    parser.add_argument("--max-polls", type=int, default=120, help="Maximum poll attempts")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    response = poll_transcription_job(
        transcription_id=args.transcription_id,
        poll_interval=args.interval,
        max_polls=args.max_polls,
    )

    if args.json:
        print(json.dumps(response.to_dict(), indent=2))
    else:
        print(format_transcript_output(response))


if __name__ == "__main__":
    main()
