from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, source_language_code: str, target_language_code: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project.
        source_language_code: The language code of the input text (e.g., "en").
        target_language_code: The language code to translate the text to (e.g., "es").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    return response.translations[0].translated_text
