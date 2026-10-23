import os


def save_audio_to_file(audio_content: bytes, file_path: str):
    """
    Writes synthesized speech audio to a local file.
    """
    try:
        with open(file_path, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file: {file_path}")
    except IOError as e:
        print(f"Error saving audio to file {file_path}: {e}")
