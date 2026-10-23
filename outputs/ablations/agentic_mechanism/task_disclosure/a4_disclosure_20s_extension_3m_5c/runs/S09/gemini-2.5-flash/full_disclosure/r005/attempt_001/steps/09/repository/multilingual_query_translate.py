
from google.cloud import translate_v3 as translate

def translate_query(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a given text into the target language using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

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

    # The response can contain multiple translations, but we expect only one for a single query.
    for translation in response.translations:
        return translation.translated_text
    return ""

