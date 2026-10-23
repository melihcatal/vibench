import os
from google.cloud import translate

def translate_document_field(text: str, target_language: str, project_id: str | None = None) -> str:
    """Translates user-facing document fields using Google Cloud Translation.

    Args:
        text: The text string to translate.
        target_language: The BCP-47 language code to translate to (e.g., "es" for Spanish).
        project_id: Your Google Cloud Project ID. If None, it will try to read from GOOGLE_CLOUD_PROJECT or rely on default credentials.

    Returns:
        The translated text.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    if not project_id:
        print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Relying on default credentials for project ID.")

    client = translate.TranslationServiceClient()

    # The location must be a global endpoint for now. Specify an alternate region for auto-detection.
    parent = f"projects/{project_id}"

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
    
    print(f"Translated text from 'auto' to '{target_language}'.")
    return translated_text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS or default credentials setup)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Set this env var or pass directly
    # if project_id:
    #     text_to_translate = "Hello, world! This is a test sentence."
    #     target_lang = "es"
    #     translated = translate_document_field(text_to_translate, target_lang, project_id)
    #     print(f"Original: {text_to_translate}")
    #     print(f"Translated ({target_lang}): {translated}")
    # else:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or ensure default credentials are configured.")
    pass
