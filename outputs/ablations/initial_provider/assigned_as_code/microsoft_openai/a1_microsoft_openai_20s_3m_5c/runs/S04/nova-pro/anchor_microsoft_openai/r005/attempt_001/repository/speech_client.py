import os
from google.cloud import speech_v1 as speech

def speech_client():
    return speech.SpeechClient()

def speech_config(enable_speaker_diarization=False, diarization_speaker_count=2):
    config = {}
    if enable_speaker_diarization:
        config['enable_speaker_diarization'] = True
        config['diarization_speaker_count'] = diarization_speaker_count
    return config