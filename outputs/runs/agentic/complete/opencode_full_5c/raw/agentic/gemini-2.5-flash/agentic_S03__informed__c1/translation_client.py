import os
from google.cloud import translate


def get_translate_client():
    """Returns a Google Cloud Translation client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return translate.TranslationServiceClient()


def get_gemini_client():
    """Returns a Google Gemini API client."""
    # GOOGLE_API_KEY environment variable should be set
    import google.generativeai as genai

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai


def get_perspective_api_key():
    """Returns the Perspective API key."""
    return os.environ.get("PERSPECTIVE_API_KEY")


def get_text_to_speech_client():
    """Returns a Google Cloud Text-to-Speech client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    from google.cloud import texttospeech

    return texttospeech.TextToSpeechClient()
