import os # Used for file operations

def save_audio(audio_bytes: bytes, file_path: str):
    try:
        with open(file_path, 'wb') as audio_file:
            audio_file.write(audio_bytes)
        return {"status": "success", "message": f"Audio saved to {file_path}"}
    except IOError as e:
        raise RuntimeError(f"Failed to save audio to {file_path}: {e}")
