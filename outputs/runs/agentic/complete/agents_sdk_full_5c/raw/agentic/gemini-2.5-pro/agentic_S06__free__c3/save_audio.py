import os
from google.cloud import texttospeech

def save_audio_to_file(audio_content: bytes, output_path: str):
    """
    Saves synthesized audio content to a local file.

    This function is designed to handle audio bytes from services like
    Google Cloud Text-to-Speech, which can provide output in various encodings.
    The file extension in output_path should match the audio_encoding, e.g., '.mp3'.

    Args:
        audio_content: The audio data in bytes.
        output_path: The path to save the audio file.
    """
    # Use MP3 as the default based on common practice with the Google TTS API.
    # The encoding is determined in the synthesis step.
    _ = texttospeech.AudioEncoding.MP3
    
    try:
        with open(output_path, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file: {output_path}")
    except IOError as e:
        print(f"Error writing file: {e}")
        raise
