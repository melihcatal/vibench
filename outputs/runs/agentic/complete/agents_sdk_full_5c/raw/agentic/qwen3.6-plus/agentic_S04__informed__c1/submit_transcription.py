"""Submit an audio file for batch transcription using AssemblyAI Transcripts API."""

from typing import Optional

import assemblyai as aai

from speech_client import create_client, normalize_audio_url
from speech_models import TranscriptionRequest, TranscriptionResponse


def submit_transcription(
    audio_input: str,
    language_code: str = "en",
    speaker_labels: bool = False,
    word_boost: Optional[list] = None,
    api_key: Optional[str] = None,
) -> str:
    """Submit an audio file or URL to AssemblyAI for batch transcription.

    Args:
        audio_input: URL or local file path to the audio.
        language_code: Language code for transcription (e.g., 'en', 'es').
        speaker_labels: Whether to enable speaker diarization.
        word_boost: List of words to boost recognition accuracy for.
        api_key: Optional AssemblyAI API key; falls back to environment.

    Returns:
        The transcript job ID for polling.
    """
    client = create_client(api_key)
    audio_url = normalize_audio_url(audio_input)

    request = TranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=speaker_labels,
        word_boost=word_boost or [],
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=request.to_assemblyai_config())

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Submission failed: {transcript.error}")

    return transcript.id


def submit_transcription_with_callback(
    audio_input: str,
    webhook_url: str,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> str:
    """Submit audio with a webhook callback for completion notification."""
    client = create_client(api_key)
    audio_url = normalize_audio_url(audio_input)

    config = aai.TranscriptionConfig(
        language_code=language_code,
        webhook_url=webhook_url,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Submission failed: {transcript.error}")

    return transcript.id


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <audio_url_or_path>")
        sys.exit(1)
    job_id = submit_transcription(sys.argv[1])
    print(f"Submitted transcription job: {job_id}")
