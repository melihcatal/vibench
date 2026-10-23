from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.cloud import language_v1
from google.cloud import speech
from google.cloud import aiplatform


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_translation_client():
    return translate.Client()


def get_language_client():
    return language_v1.LanguageServiceClient()


def get_speech_to_text_client():
    return speech.SpeechClient()


def get_aiplatform_client(project, location):
    aiplatform.init(project=project, location=location)
    return aiplatform
