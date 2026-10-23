"""
Request speaker diarization for a recorded meeting using AssemblyAI Transcripts API.

Submits or retrieves a transcription with speaker labels enabled,
producing a diarized transcript that identifies different speakers.
Requires ASSEMBLYAI_API_KEY environment variable.
"""

import sys
from typing import Optional, List

import assemblyai
from assemblyai import AssemblyAI, Transcriber, TranscriptConfig

from speech_client import get_assemblyai_client, get_audio_upload_url
from speech_models import (
    TranscriptionResult,
    DiarizedTranscript,
    Utterance,
    WordTimestamp,
)


def request_diarized_transcription(
    audio_url: str,
    speakers_expected: Optional[int] = None,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> DiarizedTranscript:
    """
    Submit audio for transcription with speaker diarization enabled.

    Creates a new transcription job with AssemblyAI speaker_labels enabled
    to identify and label different speakers in the recording.

    Args:
        audio_url: URL to the audio file or local file path.
        speakers_expected: Expected number of speakers (improves accuracy).
        language_code: IETF language code.
        api_key: Optional AssemblyAI API key override.

    Returns:
        DiarizedTranscript with speaker-labeled utterances.
    """
    client = get_assemblyai_client(api_key)

    # Upload local file if needed
    if not audio_url.startswith(("http://", "https://")):
        audio_url = get_audio_upload_url(audio_url, api_key=api_key)

    # Configure AssemblyAI transcription with speaker diarization
    config = Transcriber.Config(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,  # Enable AssemblyAI speaker diarization
        punctuate=True,
        format_text=True,
    )

    if speakers_expected is not None:
        config.speakers_expected = speakers_expected

    # Submit and wait for completion via AssemblyAI SDK
    transcript = client.transcriber.transcribe(config)

    # Poll for completion using AssemblyAI API
    while transcript.status == "queued" or transcript.status == "processing":
        transcript = client.transcriber.get_transcript(transcript.id)

    if transcript.status == "error":
        raise RuntimeError(
            f"AssemblyAI transcription failed: {transcript.error}"
        )

    # Convert response to local models
    raw_data = transcript.dict() if hasattr(transcript, "dict") else transcript.json()
    result = TranscriptionResult.from_assemblyai_response(raw_data)

    return DiarizedTranscript.from_transcription_result(result)


def get_existing_diarized_transcript(
    transcript_id: str,
    api_key: Optional[str] = None,
) -> DiarizedTranscript:
    """
    Retrieve an existing diarized transcript by job ID.

    Fetches a previously submitted AssemblyAI transcription that had
    speaker diarization enabled.

    Args:
        transcript_id: AssemblyAI transcription job ID.
        api_key: Optional AssemblyAI API key override.

    Returns:
        DiarizedTranscript with speaker-labeled utterances.
    """
    client = get_assemblyai_client(api_key)

    transcript = client.transcriber.get_transcript(transcript_id)

    if transcript.status == "error":
        raise RuntimeError(
            f"AssemblyAI transcription failed: {transcript.error}"
        )

    if transcript.status in ("queued", "processing"):
        raise RuntimeError(
            f"Transcription still processing (status: {transcript.status}). "
            f"Use poll_transcription to wait for completion."
        )

    raw_data = transcript.dict() if hasattr(transcript, "dict") else transcript.json()
    result = TranscriptionResult.from_assemblyai_response(raw_data)

    return DiarizedTranscript.from_transcription_result(result)


def format_diarized_transcript(diarized: DiarizedTranscript) -> str:
    """
    Format a diarized transcript for human-readable display.

    Args:
        diarized: DiarizedTranscript object.

    Returns:
        Formatted string with speaker labels and utterances.
    """
    lines = [f"Meeting Transcript ({len(diarized.speakers)} speakers detected)"]
    lines.append("=" * 60)

    for utterance in diarized.utterances:
        speaker_label = utterance.speaker if utterance.speaker else "Unknown"
        lines.append(f"\n[{speaker_label}]: {utterance.text}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diarized_transcript.py <audio_url_or_path> [num_speakers]")
        sys.exit(1)

    audio = sys.argv[1]
    num_speakers = int(sys.argv[2]) if len(sys.argv) > 2 else None

    result = request_diarized_transcription(audio, speakers_expected=num_speakers)
    print(format_diarized_transcript(result))
