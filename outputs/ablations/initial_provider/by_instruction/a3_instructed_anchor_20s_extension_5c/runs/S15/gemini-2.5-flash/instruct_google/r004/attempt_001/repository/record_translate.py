from google.cloud import translate_v3beta1 as translate
import os

def record_translate(text_content: str, target_language_code: str, project_id: str | None = None) -> str:
    """Translates user-facing document fields using Google Cloud Translation API.

    Args:
        text_content (str): The text content to translate.
        target_language_code (str): The language code to translate the text into (e.g., "es" for Spanish).
        project_id (str | None): The Google Cloud project ID. If None, it will be fetched from GOOGLE_CLOUD_PROJECT env var.

    Returns:
        str: The translated text.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project_id parameter not set.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        target_language_code=target_language_code,
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        print(f"Text translated successfully to {target_language_code} using Google Cloud Translation API.")
    else:
        print(f"No translation found for text to {target_language_code}.")
        
    return translated_text
