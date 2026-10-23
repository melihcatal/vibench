
from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    target_language: str,
    project_id: str,
    source_language: str = None
) -> str:
    """Translates a single piece of text into a specified language using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.
        source_language: (Optional) The language code of the input text (e.g., "en" for English).
                         If not provided, the API will attempt to auto-detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
    else:
        response = client.            translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

    for translation in response.translations:
        return translation.translated_text
    return ""

if __name__ == "__main__":
    # Example usage: Replace with your Google Cloud Project ID
    # Ensure you have set up authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    project_id = "your-gcp-project-id" 
    
    # Translate from English to Spanish
    text_to_translate = "Hello, world!"
    target_lang = "es"
    translated_text = translate_text(text_to_translate, target_lang, project_id, source_language="en")
    print(f"Original: {text_to_translate}")
    print(f"Translated to {target_lang}: {translated_text}")

    # Translate from auto-detected language to French
    text_to_translate_auto = "Bonjour le monde!"
    target_lang_auto = "en"
    translated_text_auto = translate_text(text_to_translate_auto, target_lang_auto, project_id)
    print(f"Original: {text_to_translate_auto}")
    print(f"Translated to {target_lang_auto} (auto-detected): {translated_text_auto}")
