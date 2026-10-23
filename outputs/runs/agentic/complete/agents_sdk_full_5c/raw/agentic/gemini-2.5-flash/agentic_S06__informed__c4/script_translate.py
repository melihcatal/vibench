import os
from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str, project_id: str = None) -> str:
    """Translates text using Google Cloud Translation."""
    client = translate.Client(project=project_id)

    # Target language can be a language code like 'es' for Spanish, 'fr' for French, etc.
    # https://cloud.google.com/translate/docs/languages
    result = client.translate(text, target_language=target_language)

    print(f"Text: {result['input']}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result['translatedText']

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and project_id is provided or configured.
    # Example usage:
    # text_to_translate = "Hello, how are you?"
    # translated_text = translate_script(text_to_translate, "es")
    # print(f"Translated text: {translated_text}")
    pass
