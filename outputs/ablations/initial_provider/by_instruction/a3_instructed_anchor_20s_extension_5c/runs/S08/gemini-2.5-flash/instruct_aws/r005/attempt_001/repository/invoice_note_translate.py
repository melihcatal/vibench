from google.cloud import translate_v3 as translate
import os

def translate_invoice_note(text: str, target_language_code: str = "es") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.

    Args:
        text: The text string to translate.
        target_language_code: The target language code (e.g., "es" for Spanish).

    Returns:
        The translated text string.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
