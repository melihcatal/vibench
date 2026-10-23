import os
from google.cloud import speech_v1 as speech

def diarized_transcript(audio_file):
    client = speech.SpeechClient()
    config = {
        'enable_speaker_diarization': True,
        'diarization_speaker_count': 2,
    }
    audio = {'uri': audio_file}
    response = client.long_running_recognize(config=config, audio=audio)
    return response