import os
from google.cloud import speech_v1p1beta1 as speech

def diarize_speakers(audio_file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'

    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2  # Adjust as needed
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print('Speaker Tags:', result.speaker_tags)
        print('Transcript:', result.alternatives[0].transcript)

# Example usage
# diarize_speakers('path/to/your/audiofile.wav')