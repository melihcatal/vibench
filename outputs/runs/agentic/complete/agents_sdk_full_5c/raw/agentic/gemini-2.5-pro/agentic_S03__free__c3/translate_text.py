from translation_client import get_translation_client

def translate_text(
    text: str, target_language_code: str, source_language_code: str = "en-US"
) -> str:
    """
    Translates a single text string to a target language.

    Args:
        text: The text to translate.
        target_language_code: The ISO 639-1 language code of the target language.
        source_language_code: The ISO 639-1 language code of the source language.

    Returns:
        The translated text.
    """
    client, parent = get_translation_client()

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",  # Mime type can be text/plain or text/html
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
