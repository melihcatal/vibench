"""
save_audio.py - Writes synthesized speech audio to a local file or object.

Handles persisting audio bytes from Azure Cognitive Services TTS synthesis
results to local files with appropriate format detection and metadata.
Provider: Microsoft Azure Cognitive Services Speech Service (consumes TTSResponse)
"""

import os
import json
from typing import Optional, Dict, Any

from speech_models import TTSResponse


# Azure audio format to file extension mapping
AZURE_FORMAT_EXTENSIONS = {
    "audio-16khz-32kbitrate-mono-mp3": ".mp3",
    "riff-16khz-16bit-mono-pcm": ".wav",
    "ogg-16khz-16bit-mono-opus": ".ogg",
    "flac-16khz-16bit-mono": ".flac",
    "audio-24khz-48kbitrate-mono-mp3": ".mp3",
    "riff-24khz-16bit-mono-pcm": ".wav",
    "riff-16khz-32kbitrate-mono-pcm": ".wav",
}

# MIME type to extension mapping
MIME_EXTENSIONS = {
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/ogg": ".ogg",
    "audio/flac": ".flac",
    "audio/x-flac": ".flac",
}


def save_audio_to_file(
    response: TTSResponse,
    filepath: str,
    overwrite: bool = False,
) -> Dict[str, Any]:
    """
    Write synthesized audio bytes from Azure TTS to a local file.

    Args:
        response: TTSResponse containing Azure synthesis audio bytes.
        filepath: Destination file path.
        overwrite: Whether to overwrite existing files.

    Returns:
        Dictionary with save operation metadata.
    """
    if not response.is_success():
        return {
            "success": False,
            "error": response.error_message or "Synthesis failed",
            "filepath": None,
            "bytes_written": 0,
        }

    if os.path.exists(filepath) and not overwrite:
        return {
            "success": False,
            "error": f"File already exists: {filepath}",
            "filepath": None,
            "bytes_written": 0,
        }

    try:
        with open(filepath, "wb") as f:
            bytes_written = f.write(response.audio_bytes)

        return {
            "success": True,
            "error": None,
            "filepath": os.path.abspath(filepath),
            "bytes_written": bytes_written,
            "voice_name": response.voice_name,
            "audio_format": response.audio_format,
            "content_type": response.content_type,
        }

    except IOError as exc:
        return {
            "success": False,
            "error": str(exc),
            "filepath": None,
            "bytes_written": 0,
        }


def save_audio_with_auto_extension(
    response: TTSResponse,
    base_filepath: str,
    overwrite: bool = False,
) -> Dict[str, Any]:
    """
    Write synthesized audio to a file, automatically appending the correct extension.

    Determines the file extension from the Azure TTS response content type
    and appends it to the base filepath if not already present.

    Args:
        response: TTSResponse from Azure synthesis.
        base_filepath: Base path without extension.
        overwrite: Whether to overwrite existing files.

    Returns:
        Dictionary with save operation metadata.
    """
    extension = _detect_extension(response)

    if not base_filepath.endswith(extension):
        filepath = base_filepath + extension
    else:
        filepath = base_filepath

    return save_audio_to_file(response, filepath, overwrite=overwrite)


def save_audio_to_buffer(response: TTSResponse) -> Optional[bytes]:
    """
    Extract audio bytes from Azure TTS response for in-memory use.

    Args:
        response: TTSResponse containing Azure synthesis audio bytes.

    Returns:
        Audio bytes or None if synthesis failed.
    """
    if not response.is_success():
        return None
    return response.audio_bytes


def save_audio_metadata(
    response: TTSResponse,
    metadata_filepath: str,
) -> bool:
    """
    Save Azure TTS response metadata to a JSON file.

    Args:
        response: TTSResponse from Azure synthesis.
        metadata_filepath: Path for the metadata JSON file.

    Returns:
        True if metadata was saved successfully.
    """
    metadata = {
        "voice_name": response.voice_name,
        "audio_format": response.audio_format,
        "content_type": response.content_type,
        "duration_ms": response.duration_ms,
        "request_id": response.request_id,
        "status_code": response.status_code,
        "audio_size_bytes": len(response.audio_bytes) if response.audio_bytes else 0,
    }

    try:
        with open(metadata_filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        return True
    except IOError:
        return False


def _detect_extension(response: TTSResponse) -> str:
    """Detect the appropriate file extension from the TTS response."""
    # Try content-type first
    mime = response.content_type.lower()
    if mime in MIME_EXTENSIONS:
        return MIME_EXTENSIONS[mime]

    # Try Azure format
    azure_format = response.audio_format.lower()
    if azure_format in AZURE_FORMAT_EXTENSIONS:
        return AZURE_FORMAT_EXTENSIONS[azure_format]

    # Fallback based on known format strings
    if "mp3" in azure_format or "mpeg" in mime:
        return ".mp3"
    if "wav" in azure_format or "pcm" in azure_format:
        return ".wav"
    if "ogg" in azure_format or "opus" in azure_format:
        return ".ogg"
    if "flac" in azure_format:
        return ".flac"

    return ".mp3"
