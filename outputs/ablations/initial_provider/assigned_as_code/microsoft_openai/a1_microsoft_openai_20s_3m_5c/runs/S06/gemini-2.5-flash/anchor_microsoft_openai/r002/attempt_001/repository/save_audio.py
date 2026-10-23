from speech_models import AudioSavePayload

def save_audio(payload: AudioSavePayload):
    try:
        with open(payload.file_path, 'wb') as audio_file:
            audio_file.write(payload.audio_bytes)
        return {"status": "success", "file_path": payload.file_path}
    except IOError as e:
        raise RuntimeError(f"Failed to save audio file: {e}")
