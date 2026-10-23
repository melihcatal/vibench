import os
import boto3
from storage_client import get_translate_client
from storage_models import TranslatedTextResult

def translate_text_from_document(text: str, source_language: str, target_language: str) -> TranslatedTextResult or None:
    """
    Translates text using AWS Translate.

    Args:
        text (str): The text to translate.
        source_language (str): The source language code (e.g., 'en').
        target_language (str): The target language code (e.g., 'es').

    Returns:
        TranslatedTextResult or None: The translated text and language codes, or None if an error occurs.
    """
    translate_client = get_translate_client()
    try:
        print(f"Translating text from '{source_language}' to '{target_language}'...")
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )

        translated_text = response['TranslatedText']
        actual_source_language = response['SourceLanguageCode']
        actual_target_language = response['TargetLanguageCode']

        print(f"Translation successful. Detected source: {actual_source_language}")
        return TranslatedTextResult(
            source_language_code=actual_source_language,
            target_language_code=actual_target_language,
            translated_text=translated_text
        )
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    # This example assumes you have text already extracted, e.g., from an OCR step.
    # Ensure AWS credentials are configured.

    _sample_text = (
        "The quick brown fox jumps over the lazy dog. "
        "This is a sample text for translation testing."
    )
    _source_lang = "en"
    _target_lang = "es"

    print(f"\nOriginal Text (en):\n{_sample_text}")

    translation_result = translate_text_from_document(_sample_text, _source_lang, _target_lang)

    if translation_result:
        print(f"\nTranslated Text ({translation_result.target_language_code}):\n{translation_result.translated_text}")
        print(f"Source Language Detected: {translation_result.source_language_code}")
    else:
        print("Failed to translate text.")

    # Example with German
    _sample_text_de = "Hallo Welt! Wie geht es dir heute?"
    _source_lang_de = "de"
    _target_lang_en = "en"

    print(f"\nOriginal Text (de):\n{_sample_text_de}")
    translation_result_de = translate_text_from_document(_sample_text_de, _source_lang_de, _target_lang_en)
    if translation_result_de:
        print(f"\nTranslated Text ({translation_result_de.target_language_code}):\n{translation_result_de.translated_text}")
    else:
        print("Failed to translate German text.")
