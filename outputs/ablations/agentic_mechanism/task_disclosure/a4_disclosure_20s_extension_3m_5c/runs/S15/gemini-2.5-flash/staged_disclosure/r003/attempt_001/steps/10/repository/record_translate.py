from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

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

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage:
    # Replace 'your-google-cloud-project-id' with your actual Google Cloud Project ID
    # project_id = "your-google-cloud-project-id" 
    # text_to_translate = "Hello, how are you?"
    # target_lang = "es"

    # if project_id == "your-google-cloud-project-id":
    #     print("Please replace 'your-google-cloud-project-id' with your actual Google Cloud Project ID.")
    # else:
    #     translated = translate_text(text_to_translate, target_lang, project_id)
    #     print(f"Original: {text_to_translate}")
    #     print(f"Translated ({target_lang}): {translated}")
