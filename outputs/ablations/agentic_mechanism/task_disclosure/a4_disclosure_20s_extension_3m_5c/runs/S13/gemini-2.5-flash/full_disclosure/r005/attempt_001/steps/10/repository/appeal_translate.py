
from google.cloud import translate_v3 as translate

def translate_appeal_text(text: str, project_id: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation API.

    Args:
        text: The text to translate.
        project_id: The Google Cloud project ID.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    # Return the translated text
    return response.translations[0].translated_text

