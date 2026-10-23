"""
[SAME-SCENARIO] Poll a transcription job and return the transcript.

Uses the AssemblyAI Transcripts API to check job status and retrieve
the completed transcript.
Provider: AssemblyAI Transcripts API
SDK: assemblyai
Auth: ASSEMBLYAI_API_KEY
"""

import sys
from typing import Optional

from speech_client import get_assemblyai_client, poll_with_retry
from speech_models import normalize_assemblyai_response, TranscriptResponse


def poll_transcription(
    transcript_id: str,
    max_retries: int = 60,
    poll_interval_seconds: int = 5,
    include_words: bool = True,
    include_utterances: bool = True,
) -> TranscriptResponse:
    """
    Poll an AssemblyAI transcription job until completion and return normalized results.

    Args:
        transcript_id: The transcript job ID returned from submission.
        max_retries: Maximum number of polling attempts.
        poll_interval_seconds: Seconds to wait between polls.
        include_words: Include word-level data in the response.
        include_utterances: Include speaker utterance data in the response.

    Returns:
        Normalized TranscriptResponse with full transcript text and segments.

    Raises:
        TimeoutError: If the job does not complete within the retry limit.
        assemblyai.AssemblyAIError: If the transcription job fails.
        ValueError: If transcript_id is empty or invalid.
    """
    if not transcript_id:
        raise ValueError("transcript_id must not be empty")

    client = get_assemblyai_client()

    # Poll AssemblyAI until the transcription completes
    raw_transcript = poll_with_retry(
        client=client,
        transcript_id=transcript_id,
        max_retries=max_retries,
        poll_interval_seconds=poll_interval_seconds,
    )

    # Normalize the raw AssemblyAI response
    response = normalize_assemblyai_response(raw_transcript)

    return response


def get_transcript_status(
    transcript_id: str,
) -> str:
    """
    Get the current status of an AssemblyAI transcription job.

    Args:
        transcript_id: The transcript job ID.

    Returns:
        Status string: 'queued', 'processing', 'completed', or 'error'.
    """
    client = get_assemblyai_client()
    transcript = client.transcripts.get(transcript_id)

    if hasattr(transcript.status, "value"):
        return transcript.status.value
    return str(transcript.status)


def get_transcript_text(
    transcript_id: str,
    format_text: bool = True,
) -> str:
    """
    Retrieve the plain text of a completed AssemblyAI transcription.

    Args:
        transcript_id: The transcript job ID.
        format_text: Whether to return formatted text.

    Returns:
        The full transcript as a plain text string.
    """
    response = poll_transcription(
        transcript_id=transcript_id,
        include_words=False,
        include_utterances=False,
    )
    return response.full_text


def main():
    """CLI entry point for polling a transcription job."""
    import argparse

    parser = argparse.ArgumentParser(description="Poll AssemblyAI transcription job")
    parser.add_argument("transcript_id", help="AssemblyAI transcript job ID")
    parser.add_argument("--max-retries", type=int, default=60, help="Maximum polling retries")
    parser.add_argument("--interval", type=int, default=5, help="Seconds between polls")

    args = parser.parse_args()

    response = poll_transcription(
        transcript_id=args.transcript_id,
        max_retries=args.max_retries,
        poll_interval_seconds=args.interval,
    )

    print(f"Transcript ID: {response.transcript_id}")
    print(f"Status: {response.status}")
    print(f"Language: {response.language_code}")
    print(f"Duration: {response.duration_ms}ms")
    print(f"\nFull Transcript:\n{response.full_text}")

    return response


if __name__ == "__main__":
    main()
