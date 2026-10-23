def save_audio_content_to_file(audio_content: bytes, file_path: str):
    with open(file_path, "wb") as out:
        out.write(audio_content)
    print(f"Audio content written to file: {file_path}")
