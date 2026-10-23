import os

def save_audio(audio_bytes, file_path, content_type="audio/mpeg"):
    # Determine file extension based on content_type
    if "mpeg" in content_type or "mp3" in content_type:
        extension = ".mp3"
    elif "wav" in content_type:
        extension = ".wav"
    else:
        extension = ".bin" # Default to binary if unknown

    # Ensure the file_path has the correct extension
    if not file_path.endswith(extension):
        file_path = file_path + extension

    with open(file_path, "wb") as out:
        out.write(audio_bytes)
    return {"file_path": os.path.abspath(file_path), "size": len(audio_bytes)}
