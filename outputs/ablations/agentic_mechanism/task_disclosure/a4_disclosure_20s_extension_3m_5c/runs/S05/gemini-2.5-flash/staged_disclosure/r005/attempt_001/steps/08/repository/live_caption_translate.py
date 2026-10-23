from google.cloud import translate_v3beta1 as translate

def translate_text(
    project_id: str,
    text_content: str,
    target_language: str,
    source_language: str | None = None,
) -> str:
    """Translates text into the target language.

    Args:
        project_id: The ID of the Google Cloud project.
        text_content: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English).
                         If not specified, the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        target_language_code=target_language,
        source_language_code=source_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud project ID
    PROJECT_ID = "your-gcp-project-id" 

    # Example usage:
    text_to_translate = "Hello, how are you?"
    target_lang = "es"  # Translate to Spanish
    source_lang = "en"  # Source language is English

    if PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
        print("You also need to install the Google Cloud Translation client library:")
        print("pip install google-cloud-translate")
    else:
        try:
            translated = translate_text(PROJECT_ID, text_to_translate, target_lang, source_lang)
            print(f"Original text: {text_to_translate}")
            print(f"Translated text ({target_lang}): {translated}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure you have authenticated to Google Cloud and enabled the Cloud Translation API.")
            print("For authentication, you can use 'gcloud auth application-default login'")
