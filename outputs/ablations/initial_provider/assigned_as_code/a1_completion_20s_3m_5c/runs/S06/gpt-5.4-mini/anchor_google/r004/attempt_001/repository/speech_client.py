from google.cloud import texttospeech
from google.cloud import speech_v1p1beta1 as speech


def tts_client():
    return texttospeech.TextToSpeechClient()


def stt_client():
    return speech.SpeechClient()


def default_tts_audio_config():
    return texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
