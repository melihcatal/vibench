from google.cloud import translate

def translate_text(text: str, project_id: str, source_language: str, target_language: str) -> str:
    """Translates text into the target language."""
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
    text_to_translate = "Hello, world!"
    source_lang = "en"
    target_lang = "es"

    if project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        translated_result = translate_text(text_to_translate, project_id, source_lang, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_result}")