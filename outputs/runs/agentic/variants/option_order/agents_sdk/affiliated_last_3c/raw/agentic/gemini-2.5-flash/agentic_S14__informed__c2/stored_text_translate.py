import os
import boto3
from storage_client import get_translate_client
from storage_models import TranslationResult

def translate_text_content(text: str, source_language_code: str, target_language_code: str) -> TranslationResult | None:
    """
    Translates text from a source language to a target language using Amazon Translate.
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        
        translated_text = response.get('TranslatedText')
        actual_source_language = response.get('SourceLanguageCode')

        return TranslationResult(
            translated_text=translated_text,
            source_language_code=actual_source_language,
            target_language_code=target_language_code
        )

    except Exception as e:
        print(f"Error translating text: {e}")
        return None

if __name__ == '__main__':
    # Example usage (replace with actual values)
    text_to_translate = "Hello, how are you?"
    source_lang = "en"
    target_lang = "es"

    print(f"Translating '{text_to_translate}' from {source_lang} to {target_lang}")
    translation = translate_text_content(text_to_translate, source_lang, target_lang)

    if translation:
        print(f"Translated text: {translation.translated_text}")
        print(f"Source Language: {translation.source_language_code}")
        print(f"Target Language: {translation.target_language_code}")
    else:
        print("Translation failed.")

    text_to_translate_fr = "Bonjour, comment ça va ?"
    source_lang_fr = "fr"
    target_lang_fr = "en"

    print(f"\nTranslating '{text_to_translate_fr}' from {source_lang_fr} to {target_lang_fr}")
    translation_fr = translate_text_content(text_to_translate_fr, source_lang_fr, target_lang_fr)

    if translation_fr:
        print(f"Translated text: {translation_fr.translated_text}")
        print(f"Source Language: {translation_fr.source_language_code}")
        print(f"Target Language: {translation_fr.target_language_code}")
    else:
        print("Translation failed.")
