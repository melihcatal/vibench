def save_audio(audio_content, file_path):
    with open(file_path, "wb") as file:
        file.write(audio_content)
