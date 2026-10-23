from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language: The language to translate the text to (e.g., "en", "es", "fr").

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
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage: Replace with your Google Cloud Project ID and desired text/language
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # e.g., "my-project-12345"
    text_to_translate = "Hello, world!"
    target_lang = "es"

    if project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        translated_result = translate_text(text_to_translate, project_id, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_result}")
