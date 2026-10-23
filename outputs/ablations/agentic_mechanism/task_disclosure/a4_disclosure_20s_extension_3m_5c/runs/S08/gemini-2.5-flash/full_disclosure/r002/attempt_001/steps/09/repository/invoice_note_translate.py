
from google.cloud import translate_v3beta1 as translate

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    location = "global"  # Or your preferred location

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

