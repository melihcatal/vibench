def save_audio(audio_bytes: bytes, filename: str):
    """
    Writes synthesized speech audio to a local file.
    """
    with open(filename, "wb") as f:
        f.write(audio_bytes)
