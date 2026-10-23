import os
from google.cloud import speech_v1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

client = speech.SpeechClient()

def transcribe_audio(audio_path):
    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code='en-US',
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print(f'Transcript: {result.alternatives[0].transcript}')