
from google.cloud import translate_v3 as translate

def translate_text(
    project_id: str,
    text: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates text into the target language.

    Args:
        project_id: The ID of the GCP project.
        text: The text to translate.
        target_language: The language to translate to (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1" for advanced models
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",  # Mime types: text/plain, text/html
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    # Ensure you have authenticated and enabled the Cloud Translation API
    # For example, by running `gcloud auth application-default login`
    # and `gcloud services enable translate.googleapis.com`
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID" 
    
    # Example Usage:
    text_to_translate = "This appeal needs to be reviewed as soon as possible."
    target_lang = "es"  # Translate to Spanish

    if project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
        print("Also ensure the Google Cloud Translation API is enabled and you are authenticated.")
    else:
        translated_result = translate_text(project_id, text_to_translate, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_result}")
