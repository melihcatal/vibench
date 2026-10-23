import os

from google.cloud import speech


def get_speech_client():
    return speech.SpeechClient()


def get_default_language_code():
    return os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US")


def build_recognition_config(language_code, enable_diarization=False, enable_word_time_offsets=False):
    return speech.RecognitionConfig(
        language_code=language_code,
        enable_speaker_diarization=enable_diarization,
        enable_word_time_offsets=enable_word_time_offsets,
    )
