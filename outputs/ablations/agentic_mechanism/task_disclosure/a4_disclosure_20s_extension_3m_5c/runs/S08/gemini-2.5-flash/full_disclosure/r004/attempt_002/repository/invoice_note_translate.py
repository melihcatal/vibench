from google.cloud import translate_v3 as translate

def translate_invoice_note(text: str, target_language_code: str = "en") -> str:
    """Translates extracted invoice notes or descriptions using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language_code: The language code to translate the text into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your Google Cloud Project ID
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    translated_text = response.translations[0].translated_text
    return translated_text
