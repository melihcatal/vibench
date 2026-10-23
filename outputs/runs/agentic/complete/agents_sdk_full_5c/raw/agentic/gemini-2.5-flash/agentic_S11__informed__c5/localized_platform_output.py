import os
import deepl # DeepL SDK

def translate_platform_output(text: str, target_lang: str, source_lang: str = None):
    auth_key = os.environ.get("DEEPL_AUTH_KEY") # Provider-specific environment variable

    if not auth_key:
        print("Please set the DEEPL_AUTH_KEY environment variable.")
        return None

    translator = deepl.Translator(auth_key) # Provider-specific client

    try:
        # DeepL supports automatic source language detection if source_lang is None
        result = translator.translate_text(
            text=text,
            target_lang=target_lang, # Target language, e.g., "fr" for French
            source_lang=source_lang # Optional, e.g., "en" for English
        )
        
        return {
            "translated_text": result.text,
            "source_language": result.detected_source_lang,
            "target_language": target_lang
        }
    except deepl.exceptions.DeepLException as e:
        print(f"Error translating text with DeepL: {e}")
        return None

if __name__ == '__main__':
    original_text = "The quick brown fox jumps over the lazy dog."
    target_locale = "fr" # French

    print(f"Translating '{original_text}' to '{target_locale}' using DeepL...")
    translation_result = translate_platform_output(original_text, target_locale)

    if translation_result:
        print("Translation Result:", translation_result)
        print("Translated Text:", translation_result["translated_text"])
    
    original_text_german = "Hallo Welt!"
    target_locale_english = "en-US" # English (American)
    print(f"\nTranslating '{original_text_german}' to '{target_locale_english}' using DeepL...")
    translation_result_german = translate_platform_output(original_text_german, target_locale_english)
    if translation_result_german:
        print("Translation Result:", translation_result_german)
        print("Translated Text:", translation_result_german["translated_text"])
