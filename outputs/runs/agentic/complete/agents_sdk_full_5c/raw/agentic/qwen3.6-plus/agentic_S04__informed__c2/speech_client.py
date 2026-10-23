"""
Local configuration and client helper utilities for Batch Speech-to-Text.
Provides AssemblyAI SDK client initialization, configuration loading,
and shared connection helpers.
"""

import os
from typing import Optional

import assemblyai
from assemblyai import AssemblyAIError


def get_assemblyai_client(api_key: Optional[str] = None) -> assemblyai.Client:
    """
    Create and return an AssemblyAI client configured with the provider API key.

    Args:
        api_key: Optional AssemblyAI API key. Falls back to ASSEMBLYAI_API_KEY env var.

    Returns:
        Configured assemblyai.Client instance.

    Raises:
        ValueError: If no API key is provided via parameter or environment.
    """
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError(
            "AssemblyAI API key not found. Set ASSEMBLYAI_API_KEY environment variable or pass api_key."
        )
    return assemblyai.Client(api_key=key)


def build_transcription_request(
    audio_url: str,
    language_code: str = "en",
    auto_chapters: bool = False,
    content_safety: bool = False,
    entity_detection: bool = False,
    sentiment_analysis: bool = False,
    custom_spelling: Optional[dict] = None,
    speaker_labels: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
    dual_channel: bool = False,
    word_boost: Optional[list] = None,
) -> assemblyai.TranscriptConfig:
    """
    Build a standardized AssemblyAI transcript configuration.

    Args:
        audio_url: Publicly accessible URL to the audio file.
        language_code: ISO 639-1 language code.
        auto_chapters: Enable automatic chapter detection.
        content_safety: Enable content safety labels.
        entity_detection: Enable named entity recognition.
        sentiment_analysis: Enable sentiment analysis.
        custom_spelling: Custom spelling corrections mapping.
        speaker_labels: Enable speaker diarization.
        punctuate: Add punctuation.
        format_text: Format output text.
        dual_channel: Process dual-channel audio separately.
        word_boost: List of words/phrases to boost detection confidence.

    Returns:
        AssemblyAI TranscriptConfig object ready for submission.
    """
    config = assemblyai.TranscriptConfig(
        audio_url=audio_url,
        language_code=language_code,
        auto_chapters=auto_chapters,
        content_safety=content_safety,
        entity_detection=entity_detection,
        sentiment_analysis=sentiment_analysis,
        custom_spelling=custom_spelling,
        speaker_labels=speaker_labels,
        punctuate=punctuate,
        format_text=format_text,
        dual_channel=dual_channel,
        word_boost=word_boost,
    )
    return config


def poll_with_retry(
    client: assemblyai.Client,
    transcript_id: str,
    max_retries: int = 60,
    poll_interval_seconds: int = 5,
) -> assemblyai.Transcript:
    """
    Poll an AssemblyAI transcription job until completion or max retries.

    Args:
        client: Configured AssemblyAI client.
        transcript_id: The transcript job ID returned on submission.
        max_retries: Maximum number of polling attempts.
        poll_interval_seconds: Seconds to wait between polls.

    Returns:
        Completed assemblyai.Transcript object.

    Raises:
        TimeoutError: If job does not complete within max_retries.
        AssemblyAIError: If transcription fails.
    """
    import time

    for attempt in range(max_retries):
        transcript = client.transcripts.get(transcript_id)
        if transcript.status == assemblyai.TranscriptStatus.completed:
            return transcript
        elif transcript.status == assemblyai.TranscriptStatus.error:
            raise AssemblyAIError(
                f"Transcription failed: {transcript.error or 'Unknown error'}"
            )
        time.sleep(poll_interval_seconds)

    raise TimeoutError(
        f"Transcription did not complete after {max_retries * poll_interval_seconds} seconds"
    )


def upload_local_audio(client: assemblyai.Client, local_path: str) -> str:
    """
    Upload a local audio file to AssemblyAI and return the hosted URL.

    Args:
        client: Configured AssemblyAI client.
        local_path: Path to the local audio file.

    Returns:
        AssemblyAI-hosted audio URL ready for transcription submission.
    """
    upload_url = client.files.upload(local_path)
    return upload_url
