from google.cloud import translate_v3
import os

def translate_script(text: str, project_id: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates a given text using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        project_id: The Google Cloud project ID.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (e.g., "en" for English). Defaults to "en".

    Returns:
        The translated text.
    """
    client = translate_v3.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and text)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        text_to_translate = "Hello, how are you?"
        target_lang = "es"
        translated_output = translate_script(text_to_translate, project_id, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_output}")
