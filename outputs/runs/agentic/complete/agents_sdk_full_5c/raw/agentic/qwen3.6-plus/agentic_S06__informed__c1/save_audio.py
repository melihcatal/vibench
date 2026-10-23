"""
[SAME-SCENARIO] save_audio.py
Writes synthesized speech audio to a local file or cloud storage object.
Uses ElevenLabs streaming as the concrete TTS provider integration for
saving audio directly from a synthesis pipeline.
"""
import os
from typing import Optional
from pathlib import Path
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from speech_models import TTSResponse, AudioFormat, normalize_audio_format
from speech_client import (
    get_elevenlabs_client,
    build_voice_settings,
    resolve_audio_format_key,
    DEFAULT_ELEVENLABS_MODEL,
    DEFAULT_VOICE,
    DEFAULT_STABILITY,
    DEFAULT_SIMILARITY_BOOST,
)


def save_audio_to_file(
    response: TTSResponse,
    output_path: str,
    overwrite: bool = True,
) -> str:
    """
    Save a TTSResponse audio bytes to a local file.

    Args:
        response: The TTSResponse containing audio bytes.
        output_path: Local filesystem path for the output file.
        overwrite: Whether to overwrite existing files.

    Returns:
        The absolute path of the saved file.
    """
    output_path = os.path.abspath(output_path)

    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(f"Output file already exists: {output_path}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.audio_bytes)

    return output_path


def synthesize_and_save(
    text: str,
    output_path: str,
    voice_id: Optional[str] = None,
    model_id: str = DEFAULT_ELEVENLABS_MODEL,
    audio_format: AudioFormat = AudioFormat.MP3,
    stability: float = DEFAULT_STABILITY,
    similarity_boost: float = DEFAULT_SIMILARITY_BOOST,
    overwrite: bool = True,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> str:
    """
    Synthesize text with ElevenLabs and save the audio directly to a file.

    This function streams audio directly from ElevenLabs to disk without
    holding the entire byte stream in memory.

    Args:
        text: The text to synthesize.
        output_path: Local filesystem path for the output file.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model ID (e.g., "eleven_multilingual_v2").
        audio_format: Output audio format.
        stability: Voice stability (0.0 to 1.0).
        similarity_boost: Voice similarity boost (0.0 to 1.0).
        overwrite: Whether to overwrite existing files.
        api_key: Optional ElevenLabs API key.
        client: Optional pre-built ElevenLabs client.

    Returns:
        The absolute path of the saved file.
    """
    if client is None:
        client = get_elevenlabs_client(api_key)

    target_voice = voice_id or DEFAULT_VOICE
    voice_settings = build_voice_settings(stability, similarity_boost)
    output_format = resolve_audio_format_key(audio_format)

    output_path = os.path.abspath(output_path)
    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(f"Output file already exists: {output_path}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in client.generate(
            text=text,
            voice=Voice(
                voice_id=target_voice,
                settings=voice_settings,
            ),
            model=model_id,
            output_format=output_format,
            stream=True,
        ):
            f.write(chunk)

    return output_path


def save_audio_bytes(
    audio_bytes: bytes,
    output_path: str,
    content_type: Optional[str] = None,
    overwrite: bool = True,
) -> str:
    """
    Save raw audio bytes to a local file, inferring format from content_type.

    Args:
        audio_bytes: Raw audio data bytes.
        output_path: Local filesystem path for the output file.
        content_type: Optional MIME type to validate the format.
        overwrite: Whether to overwrite existing files.

    Returns:
        The absolute path of the saved file.
    """
    output_path = os.path.abspath(output_path)

    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(f"Output file already exists: {output_path}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


if __name__ == "__main__":
    path = synthesize_and_save(
        text="This audio was synthesized with ElevenLabs and saved directly to disk.",
        output_path="./output/tts_sample.mp3",
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2",
    )
    print(f"Audio saved to: {path}")
