import os
from google.cloud import translate

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en" for English).

    Returns:
        The translated text.
    """
    # This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and points to your service account key file.
    # For more details, see:
    # https://cloud.google.com/docs/authentication/getting-started

    # Replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "YOUR_PROJECT_ID")

    if project_id == "YOUR_PROJECT_ID":
        return f"Translation service not configured. Please set GOOGLE_CLOUD_PROJECT_ID environment variable. Original text: {text}"

    client = translate.TranslationServiceClient()
    location = "global"  # Or specific region if needed

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts[0] if translated_texts else text

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT_ID environment variable before running
    # e.g., export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
    # And ensure you have authenticated with gcloud or set GOOGLE_APPLICATION_CREDENTIALS

    # For demonstration purposes, if the project ID is not set, it will return a placeholder message.
    
    text_to_translate = "Hola mundo"
    target_lang = "es"
    print(f"Original text: {text_to_translate}")
    print(f"Translating to {target_lang}...")
    translated_text = translate_text(text_to_translate, target_lang)
    print(f"Translated text: {translated_text}")

    text_to_translate_french = "Bonjour le monde"
    target_lang_english = "en"
    print(f"Original text: {text_to_translate_french}")
    print(f"Translating to {target_lang_english}...")
    translated_text_english = translate_text(text_to_translate_french, target_lang_english)
    print(f"Translated text: {translated_text_english}")
