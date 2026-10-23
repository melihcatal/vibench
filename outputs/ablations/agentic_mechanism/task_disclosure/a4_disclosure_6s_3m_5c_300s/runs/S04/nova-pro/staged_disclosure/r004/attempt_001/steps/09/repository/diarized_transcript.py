import os
from google.cloud import speech_v1p1beta1 as speech

def diarize_audio(audio_file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print('Speaker tags:', result.speaker_tags)
        alternative = result.alternatives[0]
        print('Transcript:', alternative.transcript)

if __name__ == '__main__':
    audio_file_path = 'path/to/your/audio/file.wav'
    diarize_audio(audio_file_path)