"""
Local helper utilities for AssemblyAI Batch Speech-to-Text integration.

Provides client configuration, authentication, and helper functions
for working with the AssemblyAI Transcripts API.
"""

import os
from typing import Optional, Dict, Any

import assemblyai
from assemblyai import AssemblyAI


# AssemblyAI service identifier
PROVIDER = "AssemblyAI"
PROVIDER_API_HOST = "api.assemblyai.com"


def get_assemblyai_client(api_key: Optional[str] = None) -> AssemblyAI:
    """
    Create and return an authenticated AssemblyAI client.

    Args:
        api_key: Optional AssemblyAI API key. Defaults to ASSEMBLYAI_API_KEY env var.

    Returns:
        Configured AssemblyAI client instance.
    """
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError(
            "ASSEMBLYAI_API_KEY environment variable must be set "
            "to use AssemblyAI Transcripts API"
        )
    client = AssemblyAI(api_key=key)
    return client


def build_transcription_config(
    audio_url: str,
    language_code: str = "en",
    enable_diarization: bool = False,
    diarize_speakers: Optional[int] = None,
    enable_word_timestamps: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
    speaker_labels: bool = False,
    auto_chapters: bool = False,
    entity_detection: bool = False,
    custom_spelling: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Build a transcription request configuration dict for AssemblyAI.

    Args:
        audio_url: Publicly accessible URL to the audio file.
        language_code: IETF language tag (default: 'en').
        enable_diarization: Whether to enable speaker diarization.
        diarize_speakers: Number of speakers to detect (optional).
        enable_word_timestamps: Whether to return word-level timestamps.
        punctuate: Enable automatic punctuation.
        format_text: Enable text formatting.
        speaker_labels: Enable speaker labels (alias for diarization).
        auto_chapters: Enable automatic chapter generation.
        entity_detection: Enable entity detection.
        custom_spelling: List of custom spelling overrides.

    Returns:
        Dict suitable for AssemblyAI Transcriber config.
    """
    config: Dict[str, Any] = {
        "audio_url": audio_url,
        "language_code": language_code,
        "punctuate": punctuate,
        "format_text": format_text,
    }

    if enable_diarization:
        config["speaker_labels"] = True
        if diarize_speakers is not None:
            config["speakers_expected"] = diarize_speakers

    if enable_word_timestamps:
        config["word_timestamps"] = True

    if auto_chapters:
        config["auto_chapters"] = True

    if entity_detection:
        config["entity_detection"] = True

    if custom_spelling:
        config["custom_spelling"] = custom_spelling

    return config


def normalize_transcription_response(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize an AssemblyAI transcription response into a standard format.

    Args:
        raw_response: Raw dict response from AssemblyAI API.

    Returns:
        Normalized transcription result with standardized keys.
    """
    return {
        "transcript_id": raw_response.get("id"),
        "status": raw_response.get("status", "unknown"),
        "text": raw_response.get("text", ""),
        "words": raw_response.get("words", []),
        "utterances": raw_response.get("utterances", []),
        "language": raw_response.get("language_code", ""),
        "audio_duration": raw_response.get("audio_duration"),
        "confidence": raw_response.get("confidence"),
        "chapters": raw_response.get("chapters", []),
        "entities": raw_response.get("entities", []),
        "error": raw_response.get("error"),
    }


def get_audio_upload_url(
    file_path: str, api_key: Optional[str] = None
) -> str:
    """
    Upload a local audio file to AssemblyAI's temporary storage.

    Args:
        file_path: Path to the local audio file.
        api_key: Optional AssemblyAI API key.

    Returns:
        AssemblyAI-hosted audio URL for transcription.
    """
    client = get_assemblyai_client(api_key)
    upload_url = client.files.upload(file_path)
    return upload_url
