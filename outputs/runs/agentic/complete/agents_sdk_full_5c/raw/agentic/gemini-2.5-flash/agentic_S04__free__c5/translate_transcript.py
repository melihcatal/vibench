from google.cloud import translate_v3 as translate
import os

def translate_text(text: str, target_language_code: str, project_id: str, source_language_code: Optional[str] = None) -> str:
    """Translates a given text into the target language using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.
        source_language_code: The BCP-47 language code of the source language (e.g., "en").
                              If not provided, the API will attempt to auto-detect.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global" # Or a specific region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    if source_language_code:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",  # Mime types: "text/plain", "text/html"
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )
    else:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language_code,
        )

    translated_text = response.translations[0].translated_text
    print(f"Translated text: {translated_text}")
    return translated_text

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    text_to_translate = "Hello, how are you? This is a test transcript."
    target_lang = "es" # Spanish

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        print(f"Translating \"{text_to_translate}\" to {target_lang}...")
        translated = translate_text(text_to_translate, target_lang, PROJECT_ID, source_language_code="en")
        print(f"Original: {text_to_translate}\nTranslated: {translated}")
