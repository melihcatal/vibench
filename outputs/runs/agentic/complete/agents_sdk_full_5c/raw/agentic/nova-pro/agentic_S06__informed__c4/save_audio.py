def save_audio(audio_data, file_name):
    with open(file_name, 'wb') as f:
        f.write(audio_data)