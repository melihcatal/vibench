
from google.cloud import translate_v3 as translate

def translate_text_from_stored_document(
    text_content: str,
    project_id: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates text content using the Google Cloud Translation API.

    Args:
        text_content: The text content extracted from a stored document.
        project_id: The ID of the Google Cloud project.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and text)
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    text_to_translate = "Hello, world! This is a sample text for translation."
    target_lang = "es"  # Translate to Spanish

    if project_id == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
        print("You also need to set up Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable).")
    else:
        print(f"Original text: {text_to_translate}")
        translated_result = translate_text_from_stored_document(
            text_to_translate, project_id, target_lang
        )
        print(f"Translated text ({target_lang}): {translated_result}")
