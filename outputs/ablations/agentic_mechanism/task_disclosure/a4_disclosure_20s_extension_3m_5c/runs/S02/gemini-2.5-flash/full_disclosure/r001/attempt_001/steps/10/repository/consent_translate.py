from google.cloud import translate_v3 as translate

def translate_consent_copy(text: str, target_language_code: str, project_id: str, source_language_code: str = None) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.
        source_language_code: The language code of the input text (e.g., "en" for English).
                               If not specified, the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": target_language_code,
            }
        )

    # The response can contain multiple translations, but we only sent one piece of content.
    return response.translations[0].translated_text
