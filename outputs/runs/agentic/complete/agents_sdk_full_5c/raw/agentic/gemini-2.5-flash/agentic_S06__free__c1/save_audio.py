import os

def save_audio_to_file(audio_bytes: bytes, file_path: str):
    """Writes synthesized speech audio bytes to a local file.

    Args:
        audio_bytes: The audio content as bytes.
        file_path: The full path to the local file where the audio will be saved.
    """
    try:
        with open(file_path, "wb") as out:
            out.write(audio_bytes)
        print(f"Audio content written to file: {file_path}")
    except IOError as e:
        print(f"Error saving audio to file {file_path}: {e}")
