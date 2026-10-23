import os
from google.cloud import translate

def translate_text(text: str, target_language_code: str = "es", project_id: str = None) -> str:
    """Translates a given text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()

    if project_id is None:
        # Attempt to get project ID from GOOGLE_CLOUD_PROJECT environment variable
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = " ".join([translation.translated_text for translation in response.translations])
    return translated_text

if __name__ == '__main__':
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    #              export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    example_text = "Hello world, this is a test transcript segment."
    target_lang = "fr"
    try:
        translated = translate_text(example_text, target_lang)
        print(f"Original: {example_text}")
        print(f"Translated ({target_lang}): {translated}")
    except Exception as e:
        print(f"Error translating text: {e}")
