import boto3

polly_client = boto3.client('polly')

def save_audio(audio_stream, file_path):
    with open(file_path, 'wb') as file:
        file.write(audio_stream)