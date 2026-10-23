import os
from google.cloud import speech

def diarized_transcript(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print(f'Operation name: {operation.name}')
    return operation.name