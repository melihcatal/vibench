def save_audio_to_file(audio_bytes: bytes, file_path: str):
    """Writes synthesized speech audio to a local file."""
    try:
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_bytes)
        # print(f"Audio saved successfully to {file_path}")
    except IOError as e:
        raise Exception(f"Error saving audio to file {file_path}: {e}")
