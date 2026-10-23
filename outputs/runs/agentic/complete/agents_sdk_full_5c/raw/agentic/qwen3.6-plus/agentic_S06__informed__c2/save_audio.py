"""Write synthesized speech audio to a local file or object using Google Cloud Text-to-Speech."""

import os
import io
from typing import Optional, Union, BinaryIO
from google.cloud import texttospeech
from google.cloud.texttospeech import enums

from speech_client import get_google_tts_project, AudioSaveConfig
from speech_models import TTSResponse


def save_audio_to_file(
    response: TTSResponse,
    filepath: str,
    overwrite: bool = True,
) -> str:
    """Save synthesized audio bytes to a local file via Google Cloud TTS conventions.

    Args:
        response: TTSResponse containing audio_bytes to save.
        filepath: Destination file path.
        overwrite: Whether to overwrite existing files.

    Returns:
        The filepath that was written.

    Raises:
        FileExistsError: If file exists and overwrite is False.
    """
    if not overwrite and os.path.exists(filepath):
        raise FileExistsError(f"File already exists: {filepath}")

    ext = os.path.splitext(filepath)[1].lstrip(".").lower() or "mp3"
    if ext in ("mp3", "ogg", "flac", "wav"):
        content_type = _ext_to_content_type(ext)
    else:
        content_type = response.content_type

    with open(filepath, "wb") as f:
        f.write(response.audio_bytes)

    return filepath


def save_audio_to_stream(
    response: TTSResponse,
    stream: Optional[BinaryIO] = None,
) -> Union[BinaryIO, io.BytesIO]:
    """Save synthesized audio bytes to a binary stream.

    Args:
        response: TTSResponse containing audio_bytes.
        stream: Target binary stream. If None, returns a new BytesIO.

    Returns:
        The stream containing the audio data.
    """
    target = stream if stream is not None else io.BytesIO()
    target.write(response.audio_bytes)
    target.seek(0)
    return target


def synthesize_and_save(
    text: str,
    output_path: str,
    voice_name: str = "en-US-Standard-C",
    language_code: str = "en-US",
    audio_encoding: str = "MP3",
    sample_rate_hertz: int = 24000,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> str:
    """Synthesize text via Google Cloud TTS and save directly to file.

    Args:
        text: Text to synthesize.
        output_path: Destination file path.
        voice_name: Google Cloud voice name.
        language_code: Language code (e.g., 'en-US', 'ja-JP').
        audio_encoding: Audio encoding format (MP3, LINEAR16, OGG_OPUS, etc.).
        sample_rate_hertz: Sample rate in Hz.
        speaking_rate: Speed multiplier (0.25 to 4.0).
        pitch: Pitch adjustment in semitones (-20.0 to 20.0).

    Returns:
        The output file path.
    """
    project = get_google_tts_project()

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    encoding_enum = _str_to_encoding(audio_encoding)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=encoding_enum,
        sample_rate_hertz=sample_rate_hertz,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    audio_response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    tts_response = TTSResponse(
        audio_bytes=audio_response.audio_content,
        content_type=_encoding_to_content_type(audio_encoding),
        character_count=len(text),
        voice_name=voice_name,
        model_used="google_standard_tts",
    )

    return save_audio_to_file(tts_response, output_path)


def _str_to_encoding(encoding_str: str) -> enums.SsmlVoiceGender:
    """Convert encoding string to Google Cloud TextToSpeech enum."""
    mapping = {
        "MP3": enums.AudioEncoding.MP3,
        "LINEAR16": enums.AudioEncoding.LINEAR16,
        "WAV": enums.AudioEncoding.LINEAR16,
        "OGG_OPUS": enums.AudioEncoding.OGG_OPUS,
        "OGG": enums.AudioEncoding.OGG_OPUS,
        "MULAW": enums.AudioEncoding.MULAW,
        "ALAW": enums.AudioEncoding.ALAW,
    }
    return mapping.get(encoding_str.upper(), enums.AudioEncoding.MP3)


def _encoding_to_content_type(encoding_str: str) -> str:
    """Map encoding string to MIME content type."""
    mapping = {
        "MP3": "audio/mpeg",
        "LINEAR16": "audio/wav",
        "WAV": "audio/wav",
        "OGG_OPUS": "audio/ogg",
        "OGG": "audio/ogg",
        "MULAW": "audio/basic",
        "ALAW": "audio/basic",
    }
    return mapping.get(encoding_str.upper(), "audio/mpeg")


def _ext_to_content_type(ext: str) -> str:
    """Map file extension to MIME type."""
    mapping = {
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "ogg": "audio/ogg",
        "flac": "audio/flac",
        "opus": "audio/opus",
    }
    return mapping.get(ext, "audio/mpeg")


if __name__ == "__main__":
    output = synthesize_and_save(
        "This audio was saved using Google Cloud Text-to-Speech.",
        output_path="output.mp3",
        voice_name="en-US-Standard-C",
    )
    print(f"Saved audio to {output}")
