"""
Request speaker diarization for a recorded meeting using the AssemblyAI API.

Submits an audio file with speaker_labels enabled, waits for completion,
and returns the transcript segmented by speaker.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

from speech_client import (
    create_transcription_request,
    submit_transcription_job,
    upload_audio_file,
    wait_for_completion,
)
from speech_models import normalize_transcription_response, TranscriptResult


def transcribe_with_diarization(
    audio_path: str,
    language_code: str = "en",
) -> List[Dict[str, Any]]:
    """
    Submit audio for transcription with speaker diarization enabled on AssemblyAI.

    Parameters
    ----------
    audio_path : str
        Local path to the audio file (e.g., meeting recording).
    language_code : str
        Language code for transcription.

    Returns
    -------
    list[dict]
        List of utterance segments, each containing:
        - speaker: Speaker identifier (e.g., 'Speaker A')
        - text: Transcribed text for that segment
        - start_ms: Start time in milliseconds
        - end_ms: End time in milliseconds
    """
    audio_url = upload_audio_file(audio_path)

    payload = create_transcription_request(
        audio_url=audio_url,
        speaker_labels=True,
        language_code=language_code,
        punctuate=True,
        format_text=True,
    )

    job_id = submit_transcription_job(payload)
    raw_response = wait_for_completion(job_id)

    result: TranscriptResult = normalize_transcription_response(raw_response)

    diarized_segments = []
    for utt in result.utterances:
        diarized_segments.append({
            "speaker": utt.speaker,
            "text": utt.text,
            "start_ms": utt.start,
            "end_ms": utt.end,
            "word_count": len(utt.words),
        })

    return diarized_segments


def format_diarized_output(segments: List[Dict[str, Any]]) -> str:
    """
    Format diarized segments as a readable meeting transcript.
    """
    lines = []
    for seg in segments:
        speaker_label = seg.get("speaker", "Unknown") or "Unknown"
        lines.append(f"[{speaker_label}] {seg['text']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe meeting with speaker diarization")
    parser.add_argument("audio_path", help="Path to the meeting audio file")
    parser.add_argument("--language", default="en", help="Language code")
    parser.add_argument("--format", choices=["json", "text"], default="json",
                        help="Output format")
    args = parser.parse_args()

    segments = transcribe_with_diarization(args.audio_path, args.language)

    if args.format == "json":
        print(json.dumps(segments, indent=2))
    else:
        print(format_diarized_output(segments))


if __name__ == "__main__":
    main()
