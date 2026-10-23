import os
from google.cloud import translate

def translate_output(text_content: str, target_language_code: str, project_id: str):
    """Translates platform model output to another locale using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    # The project ID and location can be specified, but typically inferred from credentials
    # or default project in the environment.
    parent = f"projects/{project_id}"

    # Provider-specific model or glossary can be used here if needed.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return translations[0] if translations else ""

if __name__ == '__main__':
    # Example usage with placeholder environment variables
    # Make sure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key
    # or set GOOGLE_CLOUD_PROJECT environment variable.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your Google Cloud project ID.")
        project_id = "your-gcp-project-id" # Placeholder for demonstration

    text_to_translate = "Hello, how are you? This is a test from the model platform."
    target_lang = "fr" # French
    
    print(f"Original text: {text_to_translate}")
    try:
        translated_text = translate_output(text_to_translate, target_lang, project_id)
        print(f"Translated text ({target_lang}): {translated_text}")
    except Exception as e:
        print(f"Error during translation: {e}")
