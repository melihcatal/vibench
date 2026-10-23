from google.cloud import translate_v3 as translate

def translate_platform_output(text: str, target_language: str, project_id: str) -> str:
    """
    Translates platform model output to a specified target language using Google Cloud Translation.

    Args:
        text: The text content to be translated.
        target_language: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
