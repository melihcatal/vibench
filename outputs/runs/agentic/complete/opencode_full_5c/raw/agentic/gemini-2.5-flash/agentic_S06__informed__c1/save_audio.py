import os


def save_audio_to_file(audio_content: bytes, filename: str):
    """
    Writes synthesized speech audio to a local file.
    """
    with open(filename, "wb") as out:
        out.write(audio_content)
