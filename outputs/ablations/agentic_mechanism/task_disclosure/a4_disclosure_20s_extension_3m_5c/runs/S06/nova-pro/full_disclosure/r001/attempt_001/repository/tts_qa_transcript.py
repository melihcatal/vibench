import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-file.json'
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__'):
    audio_file_path = 'path/to/audio_file.wav'
    transcribe_audio(audio_file_path)