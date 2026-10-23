def save_audio(audio_bytes: bytes, file_path: str):
    try:
        with open(file_path, 'wb') as f:
            f.write(audio_bytes)
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}
