def save_audio_to_file(audio_bytes: bytes, filename: str):
    """Saves the audio bytes to a local file.

    Args:
        audio_bytes: The audio content in bytes.
        filename: The path to save the audio file.
    """
    with open(filename, "wb") as out:
        out.write(audio_bytes)
        print(f'Audio content written to file "{filename}"')
