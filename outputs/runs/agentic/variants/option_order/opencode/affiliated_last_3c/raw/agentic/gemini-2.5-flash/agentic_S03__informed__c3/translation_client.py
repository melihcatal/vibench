import os
from google.cloud import translate


def get_translation_client():
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    return translate.TranslationServiceClient()


def get_gemini_client():
    # Requires GOOGLE_API_KEY environment variable to be set
    # For example: export GOOGLE_API_KEY="your_api_key"
    import google.generativeai as genai

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai


def get_text_to_speech_client():
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    from google.cloud import texttospeech

    return texttospeech.TextToSpeechClient()


def get_tisane_api_key():
    # Requires TISANE_API_KEY environment variable to be set
    return os.environ.get("TISANE_API_KEY")
