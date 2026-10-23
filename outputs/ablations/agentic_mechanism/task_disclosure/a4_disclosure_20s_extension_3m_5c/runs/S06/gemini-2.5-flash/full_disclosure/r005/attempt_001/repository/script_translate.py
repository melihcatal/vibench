from google.cloud import translate_v3beta1 as translate

def translate_script(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a given text using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    translated_text = response.translations[0].translated_text
    return translated_text

