def save_audio(audio_bytes: bytes, file_path: str):
    """
    Writes synthesized speech audio to a local file.

    Args:
        audio_bytes: The audio content as a bytes object.
        file_path: The path to the local file where the audio should be saved.
    """
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
