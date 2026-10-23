
from google.cloud import translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project.
        target_language: The language to translate to (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

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
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    text_to_translate = "Hello, world!"
    target_lang = "es"  # Translate to Spanish

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_output = translate_text(text_to_translate, YOUR_PROJECT_ID, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_output}")
