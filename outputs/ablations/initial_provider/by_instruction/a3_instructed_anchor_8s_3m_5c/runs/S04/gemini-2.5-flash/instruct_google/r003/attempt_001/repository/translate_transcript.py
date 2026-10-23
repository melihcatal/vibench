from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str, project_id: str):
    """Translates a given text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
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

    translated_text = response.translations[0].translated_text
    print(f"Translated text: {translated_text}")
    return translated_text
