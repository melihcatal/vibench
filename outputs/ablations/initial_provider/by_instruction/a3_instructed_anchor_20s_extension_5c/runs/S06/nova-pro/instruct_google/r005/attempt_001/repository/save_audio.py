def save_audio(audio_content, file_path):
    with open(file_path, 'wb') as out:
        out.write(audio_content)