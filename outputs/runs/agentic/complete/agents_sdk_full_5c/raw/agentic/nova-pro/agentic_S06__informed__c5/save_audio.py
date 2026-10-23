import boto3

def save_audio(audio_stream, file_path):
    with open(file_path, 'wb') as file:
        file.write(audio_stream)