import os
from google.cloud import translate_v2 as translate
from model_client import get_llm_client

def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate model output to target language using Google Cloud Translation.\n    Requires GOOGLE_APPLICATION_CREDENTIALS env var pointing to a service account JSON.\n    Returns translated string."""
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result['translatedText']
