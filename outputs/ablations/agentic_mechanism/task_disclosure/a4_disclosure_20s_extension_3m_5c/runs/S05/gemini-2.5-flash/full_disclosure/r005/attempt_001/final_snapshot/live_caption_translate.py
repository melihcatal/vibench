from google.cloud import translate_v3

def translate_caption(text: str, target_language: str) -> str:
    """Translates live caption text into another language using Google Cloud Translation.

    Args:
        text: The caption text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/your-project-id"  # Replace with your Google Cloud Project ID

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

