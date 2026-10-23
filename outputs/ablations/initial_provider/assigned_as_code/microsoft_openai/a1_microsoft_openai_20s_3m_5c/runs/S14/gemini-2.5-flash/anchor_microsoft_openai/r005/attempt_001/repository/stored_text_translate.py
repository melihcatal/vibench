from google.cloud import translate_v2 as translate
import os

def stored_text_translate(text: str, target_language: str, project_id: str) -> str:
    """
    Translates text using Google Cloud Translation API.
    """
    translate_client = translate.Client(project=project_id)

    # Target can be a language code.
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
