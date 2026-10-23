import os
from google.cloud import texttospeech # For identifying the provider output format
from typing import Union

def save_audio_to_file(audio_content: bytes, file_path: str):
    """
    Writes synthesized speech audio content to a local file.
    The audio_content is expected to be a byte stream, typically from a
    Google Cloud Text-to-Speech synthesize_speech response.
    """
    try:
        with open(file_path, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file: {file_path}")
    except IOError as e:
        print(f"Error writing audio to file {file_path}: {e}")
