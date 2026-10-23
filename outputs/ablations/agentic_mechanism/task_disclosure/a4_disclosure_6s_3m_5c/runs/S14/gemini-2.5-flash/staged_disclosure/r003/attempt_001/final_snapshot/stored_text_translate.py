from google.cloud import translate_v3

def translate_text(project_id: str, text: str, target_language: str) -> translate_v3.Translation:
    """Translates text into the target language."""
    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
    text_to_translate = "Hello, world!"
    target_lang = "es"  # Spanish

    if project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        translation_result = translate_text(project_id, text_to_translate, target_lang)
        print(f"Translated text: {translation_result.translated_text}")
