
from google.cloud import translate_v3 as translate

def translate_payload_text(text: str, target_language: str, project_id: str) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The target language for the translation (e.g., "es" for Spanish).
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

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

