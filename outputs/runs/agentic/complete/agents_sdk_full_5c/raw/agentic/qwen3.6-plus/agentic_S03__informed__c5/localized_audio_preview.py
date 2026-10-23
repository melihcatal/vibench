"""
localized_audio_preview.py - Generate spoken previews of translated copy using ElevenLabs Text-to-Speech API.

Provider: ElevenLabs Text-to-Speech API
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY environment variable
Voice ID: Uses default ElevenLabs voice (e.g., 'EXAVITQu4vr4xnSDxMaL' - Rachel)
"""

import io
import os
from typing import List, Optional, Union

from elevenlabs import ElevenLabs


DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # ElevenLabs default voice: Rachel
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def generate_audio_preview(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = DEFAULT_MODEL_ID,
    language_code: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bytes:
    """
    Generate a spoken audio preview of a single translated text string
    using the ElevenLabs Text-to-Speech API.

    Args:
        text: The translated text to convert to speech.
        voice_id: ElevenLabs voice ID. Defaults to Rachel (EXAVITQu4vr4xnSDxMaL).
        model_id: ElevenLabs TTS model. Defaults to 'eleven_multilingual_v2'
            which supports multiple languages.
        language_code: Optional BCP-47 language code (e.g., 'en', 'de', 'fr', 'ja')
            to guide pronunciation. ElevenLabs multilingual model auto-detects
            but this can improve accuracy.
        api_key: ElevenLabs API key. If None, reads from ELEVENLABS_API_KEY env variable.

    Returns:
        bytes: The generated audio data (MP3 format by default).

    Raises:
        ValueError: If text is empty or api_key is not available.
        elevenlabs.UnexpectedStatusError: If the ElevenLabs API request fails.
    """
    if not text or not text.strip():
        raise ValueError("Input text must not be empty.")

    elevenlabs_key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
    if not elevenlabs_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable or api_key parameter "
            "is required for ElevenLabs Text-to-Speech API."
        )

    client = ElevenLabs(api_key=elevenlabs_key)

    voice = voice_id or DEFAULT_VOICE_ID

    audio_stream = client.text_to_speech.convert(
        text=text.strip(),
        voice_id=voice,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    audio_bytes = b"".join(chunk for chunk in audio_stream)
    return audio_bytes


def generate_batch_audio_previews(
    texts: List[str],
    voice_id: Optional[str] = None,
    model_id: str = DEFAULT_MODEL_ID,
    language_code: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[bytes]:
    """
    Generate spoken audio previews for a list of translated text strings
    using the ElevenLabs Text-to-Speech API, preserving order.

    Args:
        texts: List of translated text strings to convert to speech.
        voice_id: ElevenLabs voice ID. Defaults to Rachel.
        model_id: ElevenLabs TTS model. Defaults to 'eleven_multilingual_v2'.
        language_code: Optional BCP-47 language code to guide pronunciation.
        api_key: ElevenLabs API key. If None, reads from ELEVENLABS_API_KEY env variable.

    Returns:
        List of bytes, each containing the generated audio for the corresponding text.

    Raises:
        ValueError: If texts list is empty or api_key is not available.
        elevenlabs.UnexpectedStatusError: If the ElevenLabs API request fails.
    """
    if not texts:
        raise ValueError("Input texts list must not be empty.")

    elevenlabs_key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
    if not elevenlabs_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable or api_key parameter "
            "is required for ElevenLabs Text-to-Speech API."
        )

    client = ElevenLabs(api_key=elevenlabs_key)
    voice = voice_id or DEFAULT_VOICE_ID

    audio_outputs = []

    for text in texts:
        if not text or not text.strip():
            audio_outputs.append(b"")
            continue

        audio_stream = client.text_to_speech.convert(
            text=text.strip(),
            voice_id=voice,
            model_id=model_id,
            output_format="mp3_44100_128",
        )

        audio_bytes = b"".join(chunk for chunk in audio_stream)
        audio_outputs.append(audio_bytes)

    return audio_outputs


def save_audio_to_file(
    audio_bytes: bytes,
    output_path: str,
) -> str:
    """
    Save audio bytes to a file.

    Args:
        audio_bytes: The audio data to save (MP3 format from ElevenLabs).
        output_path: File path to write the audio to.

    Returns:
        The output file path.
    """
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path
