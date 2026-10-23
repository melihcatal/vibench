from google.cloud import translate_v3 as translate
import os

def translate_text(project_id: str, text: str, target_language_code: str, source_language_code: str = None) -> str:
    """Translates extracted OCR text using Google Cloud Translation API.

    Args:
        project_id: Your Google Cloud project ID.
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (e.g., "en" for English). 
                              If None, the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # For Cloud Translation API, "global" is commonly used
    parent = f"projects/{project_id}/locations/{location}"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == '__main__':
    # Example usage placeholder
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    # if project_id:
    #     text_to_translate = "Hello world, how are you?"
    #     target_lang = "es"
    #     translated = translate_text(project_id, text_to_translate, target_lang, source_language_code="en")
    #     print(f"Original: {text_to_translate}")
    #     print(f"Translated ({target_lang}): {translated}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    pass
