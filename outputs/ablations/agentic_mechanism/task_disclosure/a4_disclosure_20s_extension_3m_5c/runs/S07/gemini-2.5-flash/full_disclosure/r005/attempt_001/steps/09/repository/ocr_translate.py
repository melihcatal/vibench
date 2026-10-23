from google.cloud import translate_v3 as translate

def translate_ocr_text(text: str, target_language: str, project_id: str, source_language: str = "en") -> str:
    """
    Translates extracted OCR text using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.
        source_language: The language of the input text (defaults to "en").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
