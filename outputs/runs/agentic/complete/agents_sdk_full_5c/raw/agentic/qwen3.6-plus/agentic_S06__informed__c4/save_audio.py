"""
Write synthesized speech audio to a local file using ElevenLabs Text to Speech integration.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

import os
from pathlib import Path
from typing import Optional, Union

from speech_client import get_elevenlabs_client
from speech_models import TTSResponse
from synthesize_text import synthesize_text


def save_audio_to_file(
    audio_bytes: bytes,
    output_path: Union[str, Path],
    format_hint: str = "mp3",
) -> Path:
    """Write audio bytes to a local file.

    Args:
        audio_bytes: Raw audio bytes from TTS synthesis.
        output_path: Destination file path.
        format_hint: Format hint for extension if not provided.

    Returns:
        Path to the written file.
    """
    path = Path(output_path)

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Add extension if missing
    if not path.suffix:
        ext_map = {
            "mp3": ".mp3",
            "wav": ".wav",
            "ogg": ".ogg",
            "flac": ".flac",
            "pcm": ".pcm",
        }
        path = path.with_suffix(ext_map.get(format_hint, ".mp3"))

    with open(path, "wb") as f:
        f.write(audio_bytes)

    return path


def synthesize_and_save(
    text: str,
    output_path: Union[str, Path],
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> dict:
    """Synthesize text and save audio to file in one step.

    Uses ElevenLabs eleven_multilingual_v2 model by default.

    Args:
        text: Plain text to synthesize.
        output_path: Destination file path.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model ID (e.g. eleven_multilingual_v2).
        api_key: ElevenLabs API key.
        stability: Voice stability.
        similarity_boost: Voice similarity.

    Returns:
        Dict with output path, file size, and synthesis metadata.
    """
    response: TTSResponse = synthesize_text(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        api_key=api_key,
        stability=stability,
        similarity_boost=similarity_boost,
    )

    saved_path = save_audio_to_file(
        response.audio_bytes,
        output_path,
        format_hint="mp3",
    )

    file_size = saved_path.stat().st_size

    return {
        "output_path": str(saved_path),
        "file_size_bytes": file_size,
        "voice_id": response.voice_id,
        "model_id": response.model_id,
        "character_count": response.character_count,
    }


def save_audio_batch(
    texts: list,
    output_dir: Union[str, Path],
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    prefix: str = "tts",
) -> list:
    """Batch synthesize and save multiple texts.

    Args:
        texts: List of text strings to synthesize.
        output_dir: Output directory for audio files.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model ID.
        api_key: ElevenLabs API key.
        prefix: Filename prefix.

    Returns:
        List of result dicts for each synthesis.
    """
    results = []
    for i, text in enumerate(texts):
        filename = f"{prefix}_{i:04d}.mp3"
        path = Path(output_dir) / filename
        result = synthesize_and_save(
            text=text,
            output_path=path,
            voice_id=voice_id,
            model_id=model_id,
            api_key=api_key,
        )
        results.append(result)
    return results
