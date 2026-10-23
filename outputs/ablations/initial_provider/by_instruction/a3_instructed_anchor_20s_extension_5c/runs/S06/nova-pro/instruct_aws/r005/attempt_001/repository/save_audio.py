def save_audio(audio_data, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_data)