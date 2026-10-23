from google.cloud import translate_v3 as translate
import os

def translate_notes(project_id: str, notes: list[str], target_language_code: str, source_language_code: str = "en") -> list[str]:
    """Translates encryption or compliance notes using Google Cloud Translation API.

    Args:
        project_id: Your Google Cloud project ID.
        notes: A list of strings (notes) to translate.
        target_language_code: The language code to translate the notes into (e.g., "es" for Spanish).
        source_language_code: The language code of the original notes (defaults to "en" for English).

    Returns:
        A list of translated notes as strings.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_texts = []
    if notes:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": notes,
                "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        for translation in response.translations:
            translated_texts.append(translation.translated_text)

    return translated_texts
