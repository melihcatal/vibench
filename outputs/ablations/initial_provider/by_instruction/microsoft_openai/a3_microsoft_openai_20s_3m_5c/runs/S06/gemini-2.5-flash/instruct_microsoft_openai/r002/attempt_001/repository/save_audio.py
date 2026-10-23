def save_audio_to_file(audio_bytes: bytes, file_path: str):
    """
    Writes synthesized speech audio (byte stream) to a local file.
    """
    try:
        with open(file_path, 'wb') as audio_file:
            audio_file.write(audio_bytes)
        print(f"Audio successfully saved to {file_path}")
    except IOError as e:
        raise IOError(f"Error saving audio to file {file_path}: {e}")
