from google.cloud import translate_v3 as translate

def translate_text(project_id: str, text: str, target_language_code: str, source_language_code: str = None) -> str:
    """
    Translates text using Google Cloud Translation.

    Args:
        project_id: The ID of the Google Cloud project.
        text: The text to translate.
        target_language_code: The BCP-47 language code of the target language.
        source_language_code: Optional. The BCP-47 language code of the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    # The response can contain multiple translations, we'll take the first one.
    if response.translations:
        return response.translations[0].translated_text
    return ""
