import boto3

def save_audio(audio_stream, file_name):
    with open(file_name, 'wb') as file:
        file.write(audio_stream)