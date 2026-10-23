import os
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import openai


def get_google_translate_client():
    """Initializes and returns a Google Cloud Translate client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    return translate.Client()


def get_openai_client():
    """Initializes and returns an OpenAI client."""
    # Assumes OPENAI_API_KEY is set in the environment
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


def get_google_tts_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    return texttospeech.TextToSpeechClient()
