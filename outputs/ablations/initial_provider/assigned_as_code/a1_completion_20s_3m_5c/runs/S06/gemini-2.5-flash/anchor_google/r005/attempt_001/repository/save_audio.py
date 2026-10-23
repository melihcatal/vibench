from speech_models import SynthesisResponse

def save_audio(audio_data: SynthesisResponse, file_path: str):
    # The audio_data.audio_bytes comes directly from Google Cloud Text-to-Speech API
    # No further provider-specific processing needed here, just writing the bytes.
    try:
        with open(file_path, "wb") as f:
            f.write(audio_data.audio_bytes)
        return {"status": "success", "file_path": file_path, "content_type": audio_data.content_type}
    except Exception as e:
        return {"status": "error", "message": str(e)}
