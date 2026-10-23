def save_audio(audio_content: bytes, file_path: str):
    """
    Writes synthesized speech audio to a local file.
    """
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_content)
