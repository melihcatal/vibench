def save_audio(audio_data, file_name):
    with open(file_name, 'wb') as file:
        file.write(audio_data)