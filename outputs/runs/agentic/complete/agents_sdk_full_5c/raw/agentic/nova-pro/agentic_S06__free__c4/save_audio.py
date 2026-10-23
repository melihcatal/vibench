def save_audio(audio_content, file_name):
    with open(file_name, 'wb') as out:
        out.write(audio_content)