def save_audio(audio_bytes: bytes, file_path: str):
    """Writes audio bytes to a local file."""
    with open(file_path, "wb") as out:
        out.write(audio_bytes)
