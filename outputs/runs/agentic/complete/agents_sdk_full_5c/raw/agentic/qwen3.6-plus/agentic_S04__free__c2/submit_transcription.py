"""
submit_transcription.py - Submits an audio file for batch transcription.

Uses AssemblyAI's batch transcription API to upload audio and initiate
a transcription job. Returns the job ID for later polling.

AssemblyAI API: https://api.assemblyai.com/v2
Model: assemblyai/nano (or default AssemblyAI model)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from speech_models import TranscriptionRequest
from speech_client import create_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def submit_audio_for_transcription(
    audio_path: str,
    language_code: str = "en",
    enable_speaker_labels: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
) -> str:
    """
    Submit an audio file for batch transcription via AssemblyAI.

    Args:
        audio_path: Path to local audio file (wav, mp3, m4a, etc.)
        language_code: Language code (default: "en")
        enable_speaker_labels: Whether to enable speaker diarization
        punctuate: Whether to punctuate the transcript
        format_text: Whether to format text (remove filler words, etc.)

    Returns:
        transcription_id: The AssemblyAI job ID for polling
    """
    client = create_client()
    try:
        # Step 1: Upload audio to AssemblyAI
        audio_path = str(Path(audio_path).resolve())
        audio_url = client.upload_audio(audio_path)
        logger.info("Audio uploaded to AssemblyAI: %s", audio_url)

        # Step 2: Create transcription request with AssemblyAI-specific parameters
        request = TranscriptionRequest(
            audio_url=audio_url,
            model="assemblyai/nano",
            speaker_labels=enable_speaker_labels,
            punctuate=punctuate,
            format_text=format_text,
            language_code=language_code,
        )

        # Step 3: Submit transcription job to AssemblyAI
        transcription_id = client.submit_transcription(request)
        logger.info("Transcription job submitted: %s", transcription_id)
        return transcription_id

    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description="Submit audio for batch transcription via AssemblyAI")
    parser.add_argument("audio_file", help="Path to audio file")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--speaker-labels", action="store_true", help="Enable speaker diarization")
    args = parser.parse_args()

    transcription_id = submit_audio_for_transcription(
        audio_path=args.audio_file,
        language_code=args.language,
        enable_speaker_labels=args.speaker_labels,
    )
    print(transcription_id)


if __name__ == "__main__":
    main()
