def save_audio(audio_content: bytes, file_path: str):
    with open(file_path, "wb") as out:
        out.write(audio_content)
