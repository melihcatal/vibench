import os
from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    target_language_code: str,
    project_id: str
) -> str:
    """Translates a given text into the target language using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID and target language
    # You can set the GOOGLE_CLOUD_PROJECT environment variable or pass it directly
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    text_to_translate = "This is a dashboard note about user activity."
    target_lang = "es"  # Spanish

    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual GCP project ID.")
    else:
        print(f"Translating: \"{text_to_translate}\" to {target_lang}")
        translated_note = translate_text(
            text=text_to_translate,
            target_language_code=target_lang,
            project_id=project_id
        )
        print(f"Translated: \"{translated_note}\"")
