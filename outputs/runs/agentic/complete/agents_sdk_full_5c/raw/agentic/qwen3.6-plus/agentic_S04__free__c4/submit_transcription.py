"""
Submit an audio file for batch transcription using the AssemblyAI API.

Uploads the audio file to AssemblyAI's upload service, then submits a
transcription job and returns the job ID for polling.
"""

from __future__ import annotations

import argparse
from typing import Optional

from speech_client import (
    create_transcription_request,
    get_headers,
    submit_transcription_job,
    upload_audio_file,
)
from speech_models import TranscriptResult


def submit_audio_for_transcription(
    audio_path: str,
    language_code: Optional[str] = "en",
    punctuate: bool = True,
    format_text: bool = True,
) -> str:
    """
    Upload an audio file and submit it for batch transcription via AssemblyAI.

    Parameters
    ----------
    audio_path : str
        Local path to the audio file.
    language_code : str, optional
        Language code for transcription (default 'en').
    punctuate : bool
        Enable automatic punctuation.
    format_text : bool
        Enable automatic text formatting.

    Returns
    -------
    str
        The AssemblyAI transcription job ID.
    """
    audio_url = upload_audio_file(audio_path)

    payload = create_transcription_request(
        audio_url=audio_url,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
    )

    job_id = submit_transcription_job(payload)
    return job_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit audio for batch transcription")
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument("--language", default="en", help="Language code")
    args = parser.parse_args()

    job_id = submit_audio_for_transcription(
        audio_path=args.audio_path,
        language_code=args.language,
    )
    print(f"Transcription job submitted. Job ID: {job_id}")


if __name__ == "__main__":
    main()
