import os
from google.cloud import speech_v1p1beta1 as speech

def diarize_speakers(audio_file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    for result in response.results:
        for alternative in result.alternatives:
            print('Transcript: {}'.format(alternative.transcript))
            for speaker in result.speaker_tags:
                print('Speaker: {}'.format(speaker))

    print('Speaker diarization complete.')

# Example usage:
# diarize_speakers('path/to/your/audio_file.wav')