def save_audio(audio_bytes, file_path):
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    return {"status": "success", "file_path": file_path}
