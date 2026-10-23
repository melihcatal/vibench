def save_audio(audio_bytes: bytes, file_path: str = None) -> str:
    if file_path:
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        return file_path
    import base64

    return base64.b64encode(audio_bytes).decode("utf-8")
