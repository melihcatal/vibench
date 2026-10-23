"""Request speaker diarization for a recorded meeting using AssemblyAI Transcripts API.

Uses the AssemblyAI Python SDK (assemblyai) with speaker_labels enabled.
Auth: ASSEMBLYAI_API_KEY environment variable.
"""

import sys
from typing import Optional, List

from assemblyai import Transcriber

from speech_client import get_default_settings, normalize_audio_source
from speech_models import (
    TranscriptionRequest,
    TranscriptionResponse,
    Segment,
    normalize_assemblyai_response,
)


def get_diarized_transcript(
    audio_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    language_code: str = "en_us",
    max_wait_seconds: int = 300,
    poll_interval: int = 5,
) -> TranscriptionResponse:
    """Submit audio for batch transcription with speaker diarization.

    Returns a TranscriptionResponse with speaker-labeled segments.
    """
    import time

    audio_src = normalize_audio_source(audio_path=audio_path, audio_url=audio_url)

    config_params = get_default_settings()
    config_params["language_code"] = language_code
    config_params["speaker_labels"] = True

    transcriber = Transcriber()
    transcript = transcriber.transcribe(audio_src, config_params)

    # Poll until completion
    while transcript.status not in ("completed", "error"):
        time.sleep(poll_interval)
        transcript = transcriber.get_transcript_by_id(transcript.id)

    if transcript.status == "error":
        raise RuntimeError(
            f"Diarized transcription failed: {transcript.error}"
        )

    return normalize_assemblyai_response(transcript)


def format_diarized_output(response: TranscriptionResponse) -> str:
    """Format diarized segments into a readable speaker-labeled transcript."""
    lines = []
    for seg in response.segments:
        speaker = seg.speaker or "Unknown"
        lines.append(f"[{speaker}] {seg.text}")
    return "\n".join(lines)


def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 else None
    audio_url = sys.argv[2] if len(sys.argv) > 2 else None

    if not audio_path and not audio_url:
        print("Usage: python diarized_transcript.py <audio_path_or_url>")
        sys.exit(1)

    result = get_diarized_transcript(audio_path=audio_path, audio_url=audio_url)
    print(f"Diarized transcript for job: {result.job_id}")
    print(format_diarized_output(result))


if __name__ == "__main__":
    main()
