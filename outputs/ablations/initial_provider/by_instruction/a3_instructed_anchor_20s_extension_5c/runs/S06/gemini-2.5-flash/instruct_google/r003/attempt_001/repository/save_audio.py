def save_audio(audio_content: bytes, file_path: str):
    """
    Writes synthesized speech audio to a local file.
    """
    try:
        with open(file_path, "wb") as out:
            out.write(audio_content)
        return {"status": "success", "message": f"Audio content written to {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
