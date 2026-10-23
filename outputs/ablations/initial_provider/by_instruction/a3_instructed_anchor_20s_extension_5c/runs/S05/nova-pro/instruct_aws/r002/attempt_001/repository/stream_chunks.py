import boto3

def stream_chunks():
    client = boto3.client('transcribe', region_name='us-west-2')
    with open('audio_file.wav', 'rb') as audio_file:
        audio_chunk = audio_file.read(1024)
        while audio_chunk:
            yield {'AudioChunk': audio_chunk}
            audio_chunk = audio_file.read(1024)