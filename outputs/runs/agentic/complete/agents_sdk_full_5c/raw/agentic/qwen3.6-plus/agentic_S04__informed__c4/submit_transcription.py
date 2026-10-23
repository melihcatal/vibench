"""Submit an audio file for batch transcription using AssemblyAI Transcripts API.

Uses the AssemblyAI Python SDK (assemblyai) to submit audio for transcription.
Auth: ASSEMBLYAI_API_KEY environment variable.
"""

import sys
from typing import Optional

from assemblyai import Transcriber

from speech_client import get_default_settings, normalize_audio_source
from speech_models import TranscriptionRequest


def submit_transcription(
    audio_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    language_code: str = "en_us",
    speaker_labels: bool = False,
) -> dict:
    """Submit an audio file to AssemblyAI for batch transcription.

    Returns a dict with the transcription id and initial status.
    """
    audio_src = normalize_audio_source(audio_path=audio_path, audio_url=audio_url)

    config_params = get_default_settings()
    config_params["language_code"] = language_code
    if speaker_labels:
        config_params["speaker_labels"] = True

    transcriber = Transcriber()
    transcript = transcriber.transcribe(audio_src, config_params)

    return {
        "job_id": transcript.id,
        "status": transcript.status,
        "audio_source": audio_src,
        "language_code": language_code,
    }


def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 else None
    audio_url = sys.argv[2] if len(sys.argv) > 2 else None

    result = submit_transcription(
        audio_path=audio_path,
        audio_url=audio_url,
        language_code="en_us",
        speaker_labels=False,
    )
    print(f"Submitted transcription job: {result['job_id']}")
    print(f"Status: {result['status']}")


if __name__ == "__main__":
    main()
