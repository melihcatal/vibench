"""
Poll a transcription job and return the transcript using the AssemblyAI API.

Retrieves the status of a transcription job and, once complete, normalizes
and returns the transcript text and metadata.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from speech_client import get_transcription_status, wait_for_completion
from speech_models import normalize_transcription_response, TranscriptResult


def poll_transcription_job(
    job_id: str,
    timeout: float = 300.0,
    poll_interval: float = 3.0,
) -> Dict[str, Any]:
    """
    Poll an AssemblyAI transcription job until it completes.

    Parameters
    ----------
    job_id : str
        The AssemblyAI transcription job ID.
    timeout : float
        Maximum time to wait in seconds.
    poll_interval : float
        Seconds between polling attempts.

    Returns
    -------
    dict
        Normalized transcript result with text, confidence, words, and utterances.
    """
    raw_response = wait_for_completion(
        job_id=job_id,
        timeout=timeout,
        poll_interval=poll_interval,
    )

    result: TranscriptResult = normalize_transcription_response(raw_response)
    return {
        "job_id": result.job_id,
        "text": result.text,
        "confidence": result.confidence,
        "language_code": result.language_code,
        "audio_duration": result.audio_duration,
        "word_count": len(result.words),
        "utterance_count": len(result.utterances),
    }


def get_transcript_text(job_id: str) -> str:
    """
    Retrieve the full transcript text from a completed AssemblyAI job.
    """
    raw = wait_for_completion(job_id)
    result = normalize_transcription_response(raw)
    return result.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Poll transcription job status")
    parser.add_argument("job_id", help="AssemblyAI transcription job ID")
    parser.add_argument("--timeout", type=float, default=300.0, help="Poll timeout in seconds")
    args = parser.parse_args()

    result = poll_transcription_job(args.job_id, timeout=args.timeout)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
