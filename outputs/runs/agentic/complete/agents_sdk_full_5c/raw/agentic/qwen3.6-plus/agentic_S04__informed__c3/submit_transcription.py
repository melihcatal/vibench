"""
Submit an audio file for batch transcription using AssemblyAI Transcripts API.

Uses the AssemblyAI SDK to upload audio and create a transcription job.
Requires ASSEMBLYAI_API_KEY environment variable.
"""

import os
import sys
from typing import Optional

import assemblyai
from assemblyai import AssemblyAI, Transcriber, TranscriptConfig

from speech_client import get_assemblyai_client, get_audio_upload_url
from speech_models import TranscriptionRequest, TranscriptionResult


def submit_transcription(
    audio_url: str,
    language_code: str = "en",
    enable_diarization: bool = False,
    diarize_speakers: Optional[int] = None,
    enable_word_timestamps: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
    auto_chapters: bool = False,
    entity_detection: bool = False,
    api_key: Optional[str] = None,
) -> TranscriptionResult:
    """
    Submit an audio file to AssemblyAI for batch transcription.

    Creates a transcription job and returns the initial result with job ID.
    The job will process asynchronously; use poll_transcription to check status.

    Args:
        audio_url: Publicly accessible URL to the audio file, or local file path.
        language_code: IETF language code (default: 'en').
        enable_diarization: Enable speaker diarization.
        diarize_speakers: Expected number of speakers.
        enable_word_timestamps: Enable word-level timestamps.
        punctuate: Enable automatic punctuation.
        format_text: Enable text formatting.
        auto_chapters: Enable automatic chapter detection.
        entity_detection: Enable entity detection.
        api_key: Optional AssemblyAI API key override.

    Returns:
        TranscriptionResult with job ID and initial status.

    Raises:
        ValueError: If ASSEMBLYAI_API_KEY is not configured.
        Exception: If the transcription submission fails.
    """
    client = get_assemblyai_client(api_key)

    # Handle local file upload if not already a URL
    if not audio_url.startswith(("http://", "https://")):
        audio_url = get_audio_upload_url(audio_url, api_key=api_key)

    # Build AssemblyAI Transcriber config
    config = Transcriber.Config(
        audio_url=audio_url,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
        speaker_labels=enable_diarization,
        word_timestamps=enable_word_timestamps,
        auto_chapters=auto_chapters,
        entity_detection=entity_detection,
    )

    if diarize_speakers is not None:
        config.speakers_expected = diarize_speakers

    # Submit transcription job via AssemblyAI SDK
    transcript = client.transcriber.transcribe(config)

    # Convert to local model
    result = TranscriptionResult.from_assemblyai_response(
        transcript.dict() if hasattr(transcript, "dict") else transcript.json()
    )
    return result


def submit_transcription_from_file(
    file_path: str,
    language_code: str = "en",
    enable_diarization: bool = False,
    api_key: Optional[str] = None,
) -> TranscriptionResult:
    """
    Convenience wrapper to submit a local audio file for transcription.

    Uploads the file to AssemblyAI's temporary storage and starts transcription.

    Args:
        file_path: Path to local audio file.
        language_code: IETF language code.
        enable_diarization: Enable speaker diarization.
        api_key: Optional AssemblyAI API key override.

    Returns:
        TranscriptionResult with job ID.
    """
    # Upload file to AssemblyAI
    audio_url = get_audio_upload_url(file_path, api_key=api_key)

    return submit_transcription(
        audio_url=audio_url,
        language_code=language_code,
        enable_diarization=enable_diarization,
        api_key=api_key,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <audio_url_or_path>")
        sys.exit(1)

    audio_source = sys.argv[1]
    result = submit_transcription(audio_source)
    print(f"Transcription submitted: {result.transcript_id}")
    print(f"Status: {result.status.value}")
