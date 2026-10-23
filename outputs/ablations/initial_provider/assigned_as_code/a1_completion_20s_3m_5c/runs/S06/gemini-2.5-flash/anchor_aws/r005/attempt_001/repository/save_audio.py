import os

def save_audio_to_file(audio_bytes: bytes, file_path: str):
    try:
        with open(file_path, "wb") as out_file:
            out_file.write(audio_bytes)
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}
