import os

def save_audio(audio_result, file_path):
    if not isinstance(audio_result.audio_data, bytes):
        raise TypeError("audio_result.audio_data must be bytes.")
    
    try:
        with open(file_path, 'wb') as audio_file:
            audio_file.write(audio_result.audio_data)
        return {"status": "success", "file_path": file_path}
    except IOError as e:
        raise RuntimeError(f"Failed to save audio to {file_path}: {e}")