"""Writes synthesized speech audio to a local file or object."""

import os
import tempfile
from typing import Optional

from speech_client import get_output_dir
from speech_models import TTSResponse, build_audio_metadata


def save_audio_to_file(
    response: TTSResponse,
    filename: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> str:
    """Save synthesized audio from a TTSResponse to a local file.

    Writes audio bytes produced by ElevenLabs synthesis to a file on disk.
    The file extension is inferred from the response content_type.
    """
    directory = get_output_dir(output_dir)

    if filename is None:
        ext = _extension_from_content_type(response.content_type)
        filename = f"tts_{response.voice_id}_{_timestamp_id()}{ext}"

    filepath = os.path.join(directory, filename)

    with open(filepath, "wb") as f:
        f.write(response.audio_bytes)

    metadata = build_audio_metadata(response)
    metadata["filepath"] = filepath
    _write_metadata(filepath, metadata)

    return filepath


def save_audio_to_tempfile(
    response: TTSResponse,
    suffix: Optional[str] = None,
) -> str:
    """Save synthesized audio to a named temporary file and return its path.

    Creates a temporary file for ElevenLabs-generated audio that is automatically
    cleaned up when the caller is done with it.
    """
    ext = suffix or _extension_from_content_type(response.content_type)
    fd, filepath = tempfile.mkstemp(suffix=ext, prefix="tts_")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(response.audio_bytes)
    except Exception:
        os.unlink(filepath)
        raise
    return filepath


def save_audio_bytes(
    response: TTSResponse,
    target_path: str,
) -> str:
    """Write audio bytes directly to the specified target path.

    Persists ElevenLabs audio output to any writable filesystem path.
    """
    with open(target_path, "wb") as f:
        f.write(response.audio_bytes)
    return target_path


def _extension_from_content_type(content_type: str) -> str:
    """Map a content-type string to a file extension."""
    mapping = {
        "audio/mpeg": ".mp3",
        "audio/wav": ".wav",
        "audio/pcm": ".pcm",
        "audio/basic": ".ul",
        "audio/ogg": ".ogg",
        "audio/flac": ".flac",
        "audio/webm": ".webm",
    }
    return mapping.get(content_type, ".bin")


def _timestamp_id() -> str:
    """Generate a simple timestamp-based unique identifier for filenames."""
    import time
    return str(int(time.time() * 1000))


def _write_metadata(audio_path: str, metadata: dict) -> None:
    """Write a sidecar metadata JSON file alongside the audio file."""
    import json
    meta_path = audio_path + ".meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, default=str)
