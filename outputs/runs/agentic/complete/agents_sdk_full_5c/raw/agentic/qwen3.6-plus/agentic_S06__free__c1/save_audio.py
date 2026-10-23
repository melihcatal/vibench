"""
save_audio.py - Writes synthesized speech audio to a local file or object.

Works with audio bytes produced by ElevenLabs TTS synthesis.
Supports MP3, PCM, and other ElevenLabs output formats.
"""

import io
import os
from pathlib import Path
from typing import BinaryIO, Optional, Union

from speech_models import TTSResponse


# File extension mapping for ElevenLabs output formats
FORMAT_EXTENSIONS = {
    "mp3_22050_32": ".mp3",
    "mp3_44100_32": ".mp3",
    "mp3_44100_64": ".mp3",
    "mp3_44100_128": ".mp3",
    "pcm_16000": ".pcm",
    "pcm_22050": ".pcm",
    "ulaw_8000": ".ulaw",
    "alaw_8000": ".alaw",
    "opus_48000_32": ".opus",
    "opus_48000_64": ".opus",
}


def save_audio_to_file(
    response: TTSResponse,
    output_path: Union[str, Path],
    overwrite: bool = False,
) -> Path:
    """Save synthesized audio from a TTSResponse to a local file.

    Args:
        response: TTSResponse containing audio bytes from ElevenLabs.
        output_path: Destination file path.
        overwrite: If True, overwrite existing file. Default: False.

    Returns:
        Path to the saved audio file.

    Raises:
        FileExistsError: If the file exists and overwrite is False.
        ValueError: If audio bytes are empty.
    """
    if not response.audio_bytes:
        raise ValueError("Cannot save empty audio response.")

    output_path = Path(output_path)

    # Auto-detect extension from format if not provided
    if not output_path.suffix:
        ext = FORMAT_EXTENSIONS.get(response.content_type, ".mp3")
        output_path = output_path.with_suffix(ext)

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.audio_bytes)

    return output_path


def save_audio_bytes_to_file(
    audio_bytes: bytes,
    output_path: Union[str, Path],
    format_hint: str = "mp3_44100_128",
    overwrite: bool = False,
) -> Path:
    """Save raw audio bytes to a local file.

    Args:
        audio_bytes: Raw audio byte stream from ElevenLabs.
        output_path: Destination file path.
        format_hint: ElevenLabs format string for extension detection.
        overwrite: If True, overwrite existing file.

    Returns:
        Path to the saved audio file.
    """
    if not audio_bytes:
        raise ValueError("Cannot save empty audio bytes.")

    output_path = Path(output_path)

    if not output_path.suffix:
        ext = FORMAT_EXTENSIONS.get(format_hint, ".mp3")
        output_path = output_path.with_suffix(ext)

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


def save_audio_to_buffer(response: TTSResponse) -> io.BytesIO:
    """Save synthesized audio to an in-memory BytesIO buffer.

    Args:
        response: TTSResponse containing audio bytes.

    Returns:
        BytesIO buffer with audio data, positioned at the start.
    """
    if not response.audio_bytes:
        raise ValueError("Cannot save empty audio response.")

    buffer = io.BytesIO(response.audio_bytes)
    buffer.seek(0)
    return buffer


def save_audio_batch(
    responses: list,
    output_dir: Union[str, Path],
    naming_prefix: str = "speech",
    overwrite: bool = False,
) -> list:
    """Save multiple TTSResponse objects to a directory.

    Args:
        responses: List of TTSResponse objects to save.
        output_dir: Destination directory path.
        naming_prefix: Prefix for output filenames.
        overwrite: If True, overwrite existing files.

    Returns:
        List of saved file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for i, response in enumerate(responses):
        filename = f"{naming_prefix}_{i:04d}{FORMAT_EXTENSIONS.get(response.content_type, '.mp3')}"
        file_path = output_dir / filename
        saved_path = save_audio_to_file(response, file_path, overwrite=overwrite)
        saved_paths.append(saved_path)

    return saved_paths


def get_file_size(path: Union[str, Path]) -> int:
    """Get the size of a saved audio file in bytes.

    Args:
        path: Path to the audio file.

    Returns:
        File size in bytes.
    """
    return Path(path).stat().st_size


def detect_format_from_file(path: Union[str, Path]) -> Optional[str]:
    """Detect the ElevenLabs format from a file extension.

    Args:
        path: Path to the audio file.

    Returns:
        ElevenLabs format string or None if unknown.
    """
    ext = Path(path).suffix.lower()
    for fmt, file_ext in FORMAT_EXTENSIONS.items():
        if file_ext == ext:
            return fmt
    return None


if __name__ == "__main__":
    from synthesize_text import synthesize_text

    sample_text = "This audio will be saved to a local file using ElevenLabs."
    response = synthesize_text(sample_text)

    output_path = save_audio_to_file(response, "output/sample.mp3", overwrite=True)
    print(f"Saved audio to: {output_path}")
    print(f"File size: {get_file_size(output_path)} bytes")
    print(f"Detected format: {detect_format_from_file(output_path)}")
