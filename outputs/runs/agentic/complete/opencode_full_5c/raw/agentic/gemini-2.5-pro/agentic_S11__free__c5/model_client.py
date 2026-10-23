import os
import cohere
from google.oauth2 import service_account
from googleapiclient import discovery
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech


def get_cohere_client() -> cohere.Client:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)


def get_perspective_client() -> discovery.Resource:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def get_google_translate_client() -> translate.Client:
    return translate.Client()


def get_google_tts_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()
