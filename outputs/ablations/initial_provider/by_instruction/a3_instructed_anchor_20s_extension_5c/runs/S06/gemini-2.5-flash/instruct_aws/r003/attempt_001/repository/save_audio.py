def save_audio(audio_bytes: bytes, output_filepath: str):
    """
    Saves audio bytes to a local file.
    """
    with open(output_filepath, "wb") as f:
        f.write(audio_bytes)
