def save_audio(audio_content, file_path):
    with open(file_path, 'wb') as out_file:
        out_file.write(audio_content)