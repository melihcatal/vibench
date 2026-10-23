import os
from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    return speech.SpeechClient()

def build_recognition_config(
    diarization_enabled: bool,
    enable_word_time_offsets: bool,
    language_code: str = "en-US",
    speaker_count_min: int = 2,
    speaker_count_max: int = 6
) -> speech.RecognitionConfig:
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_word_time_offsets=enable_word_time_offsets,
    )

    if diarization_enabled:
        config.enable_speaker_diarization = True
        config.diarization_speaker_count_min = speaker_count_min
        config.diarization_speaker_count_max = speaker_count_max
        
    return config

def build_recognition_audio(gcs_uri: str) -> speech.RecognitionAudio:
    return speech.RecognitionAudio(uri=gcs_uri)