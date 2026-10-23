import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language_code: str = "en", source_language_code: str = ""): # source_language_code can be auto-detected
    """
    Translates the input text using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    location = "global"  # For general translation
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code, # Optional, if empty, auto-detect
            "mime_type": "text/plain",
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return translations

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    text_to_translate = "Hola mundo"
    target_lang = "es"
    source_lang = "en"

    if project_id:
        translated_texts = translate_text(text_to_translate, project_id, target_lang, source_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_texts[0] if translated_texts else 'N/A'}")

        text_to_translate_auto = "Bonjour le monde"
        translated_texts_auto = translate_text(text_to_translate_auto, project_id, target_lang)
        print(f"Original text: {text_to_translate_auto}")
        print(f"Translated text (auto-detect to {target_lang}): {translated_texts_auto[0] if translated_texts_auto else 'N/A'}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
