
from google.cloud import translate_v3 as translate

def translate_text_from_storage(
    text: str,
    target_language_code: str,
    project_id: str
) -> str:
    """Translates text extracted from a stored document using Google Cloud Translation.

    Args:
        text: The text content to be translated.
        target_language_code: The BCP-47 language code to translate the text into (e.g., "fr" for French).
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
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

