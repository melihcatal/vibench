
from google.cloud import translate_v3 as translate

def translate_text_for_locale(text: str, project_id: str, target_language: str) -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML input
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    # Replace with the target language code (e.g., "es" for Spanish, "fr" for French)
    TARGET_LOCALE = "es"

    model_output_text = "Hello, welcome to our platform!"
    translated_output = translate_text_for_locale(
        model_output_text, YOUR_PROJECT_ID, TARGET_LOCALE
    )
    print(f"Original text: {model_output_text}")
    print(f"Translated text ({TARGET_LOCALE}): {translated_output}")
