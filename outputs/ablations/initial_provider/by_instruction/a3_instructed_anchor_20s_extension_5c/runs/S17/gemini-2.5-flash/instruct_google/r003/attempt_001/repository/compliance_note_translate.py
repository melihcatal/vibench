from google.cloud import translate_v2 as translate
from security_client import TranslateClientWrapper

def translate_note(text: str, target_language: str, project_id: str) -> dict:
    """Translates encryption or compliance notes for reviewers using Google Cloud Translation API.

    Args:
        text: The text of the note to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID (required for client instantiation).

    Returns:
        A dictionary containing the translated text, detected source language, and other info.
    """
    client_wrapper = TranslateClientWrapper()
    translate_client = client_wrapper.client

    result = translate_client.translate(text, target_language=target_language, project_id=project_id)

    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "input": result["input"],
    }
