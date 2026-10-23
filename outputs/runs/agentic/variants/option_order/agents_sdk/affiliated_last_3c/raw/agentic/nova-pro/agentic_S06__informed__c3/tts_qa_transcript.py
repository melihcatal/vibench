import os
from google.cloud import speech_v1 as speech

def transcribe_audio(audio_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()
    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    response = client.recognize(config=config, audio=audio)
    return ' '.join([result.alternatives[0].transcript for result in response.results])