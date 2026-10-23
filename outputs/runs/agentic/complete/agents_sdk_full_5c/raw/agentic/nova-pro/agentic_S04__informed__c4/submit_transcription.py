import os
from google.cloud import speech_v1 as speech

def submit_transcription(file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()
    with open(file_path, 'rb') as audio_file:
        input_audio = audio_file.read()
    audio = speech.RecognitionAudio(content=input_audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print('Operation name: {}'.format(operation.name))
    return operation.name