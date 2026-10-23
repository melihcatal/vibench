import os

from google.cloud import translate

from document_client import GoogleCloudClients
from document_models import TranslatedText


def translate_text(
    text: str, target_language_code: str, source_language_code: str = None
) -> TranslatedText:
    """Translates extracted OCR text using Google Cloud Translation AI.

    Args:
        text: The text content to translate.
        target_language_code: The BCP-47 language code to translate to (e.g., 'en' for English).
        source_language_code: Optional. The BCP-47 language code of the input text.
                              If not provided, the API will attempt to detect the language.

    Returns:
        A TranslatedText object containing the translated content and detected source language.
    """
    client = GoogleCloudClients.get_translation_client()

    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable must be set.")

    parent = f"projects/{project_id}"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

    translations = response.translations
    if translations:
        translated_content = translations[0].translated_text
        detected_language_code = translations[0].detected_language_code
        return TranslatedText(
            translated_content=translated_content,
            detected_language_code=detected_language_code,
        )
    else:
        return TranslatedText(
            translated_content="", detected_language_code=source_language_code
        )
