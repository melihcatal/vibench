from google.cloud import translate_v3 as translate


def translate_alt_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates generated image descriptions using Google Cloud Translation AI.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: Your Google Cloud Project ID.

    Returns:
        The translated text.
    """
    # Provider: Google Cloud Translation AI
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
