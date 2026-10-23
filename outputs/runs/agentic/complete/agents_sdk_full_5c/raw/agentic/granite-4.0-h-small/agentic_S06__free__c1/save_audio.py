import os
import io
import json
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient
from .speech_models import AudioEncoding

def save_audio(audio_bytes: bytes, output_path: str, encoding: AudioEncoding = AudioEncoding.MP3) -> None:
    """Write synthesized speech audio to a local file.

    Supports MP3 and WAV encodings.
    """
    if encoding == AudioEncoding.MP3:
        with io.open(output_path, 'wb') as f:
            f.write(audio_bytes)
    elif encoding == AudioEncoding.LINEAR16:
        # Assume caller provided PCM bytes; write as-is
        with io.open(output_path, 'wb') as f:
            f.write(audio_bytes)
    else:
        raise ValueError(f'Unsupported encoding: {encoding}')
