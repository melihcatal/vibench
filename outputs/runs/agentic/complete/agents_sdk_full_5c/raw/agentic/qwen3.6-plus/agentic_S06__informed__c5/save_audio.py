"""Write synthesized speech audio to a local file or object using ElevenLabs TTS."""

import os
from pathlib import Path
from typing import Optional, Union

from elevenlabs import ElevenLabs

from speech_client import create_elevenlabs_client, DEFAULT_MODEL, DEFAULT_VOICE_ID
from speech_models import TTSResponse


def save_audio_to_file(
    tts_response: TTSResponse,
    output_path: Union[str, Path],
    *,
    overwrite: bool = False,
) -> Path:
    """Write synthesized TTS audio bytes to a local file.

    Saves the audio payload from a TTSResponse to disk. The file extension
    is derived from the response content type if not already specified.

    Args:
        tts_response: The TTS response containing audio bytes.
        output_path: Destination file path on the local filesystem.
        overwrite: Whether to overwrite an existing file.

    Returns:
        Path to the written audio file.

    Raises:
        FileExistsError: If the file exists and overwrite is False.
    """
    path = Path(output_path)

    if path.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)

    ext = tts_response.file_extension
    if path.suffix == "":
        path = path.with_suffix(ext)

    path.write_bytes(tts_response.audio_bytes)
    return path


def synthesize_and_save(
    text: str,
    output_path: Union[str, Path],
    *,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL,
    overwrite: bool = False,
    client: Optional[ElevenLabs] = None,
) -> Path:
    """Synthesize text to speech using ElevenLabs and save directly to a file.

    Combines TTS generation via the ElevenLabs SDK with file I/O in a single call.

    Args:
        text: Plain text to synthesize.
        output_path: Destination file path for the audio output.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs model identifier (eleven_multilingual_v2).
        overwrite: Whether to overwrite an existing file.
        client: Optional pre-configured ElevenLabs client.

    Returns:
        Path to the saved audio file.
    """
    if client is None:
        client = create_elevenlabs_client()

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
        text=text,
    )

    audio_bytes = b"".join(chunk for chunk in audio_stream)

    response = TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_id=model_id,
        voice_id=voice_id,
        character_count=len(text),
    )

    return save_audio_to_file(response, output_path, overwrite=overwrite)
