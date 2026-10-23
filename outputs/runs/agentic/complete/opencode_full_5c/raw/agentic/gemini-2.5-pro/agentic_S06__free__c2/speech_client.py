import os
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.cloud import speech
import cohere
from googleapiclient import discovery


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_translation_client():
    return translate.Client()


def get_speech_client():
    return speech.SpeechClient()


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(api_key)
