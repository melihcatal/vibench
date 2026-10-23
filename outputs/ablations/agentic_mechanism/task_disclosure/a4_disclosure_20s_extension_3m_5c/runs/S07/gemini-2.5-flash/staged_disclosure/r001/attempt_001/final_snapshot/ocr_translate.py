
from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    project_id: str,
    source_language_code: str,
    target_language_code: str
) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project.
        source_language_code: The BCP-47 language code of the input text.
        target_language_code: The BCP-47 language code to translate the text to.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML input
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "your-gcp-project-id"
    text_to_translate = "Hello, world!"
    source_lang = "en"
    target_lang = "es"

    if project_id == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
        print("Ensure you have authenticated Google Cloud, e.g., by setting GOOGLE_APPLICATION_CREDENTIALS.")
    else:
        translated = translate_text(text_to_translate, project_id, source_lang, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated}")
