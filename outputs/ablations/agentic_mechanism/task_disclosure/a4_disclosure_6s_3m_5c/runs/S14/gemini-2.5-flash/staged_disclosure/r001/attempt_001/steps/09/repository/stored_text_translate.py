from google.cloud import translate_v2 as translate

def translate_text_from_storage(text_content: str, target_language: str, project_id: str) -> str:
    """Translates text content using Google Cloud Translation.

    Args:
        text_content: The text extracted from a stored document.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.Client(project=project_id)

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = client.translate(text_content, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Replace with your actual text content, target language, and project ID
    text_to_translate = "Hello, world! This is a sample text for translation."
    target_lang = "es"  # Translate to Spanish
    your_project_id = "your-gcp-project-id"  # e.g., "my-gcp-project-12345"

    try:
        translated_text = translate_text_from_storage(text_to_translate, target_lang, your_project_id)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_text}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated with Google Cloud and enabled the Translation API.")
        print("You might need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable or run 'gcloud auth application-default login'.")
