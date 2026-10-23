import os


def save_audio_to_file(audio_content: bytes, file_path: str):
    """
    Writes synthesized speech audio to a local file.
    """
    with open(file_path, "wb") as out:
        out.write(audio_content)
