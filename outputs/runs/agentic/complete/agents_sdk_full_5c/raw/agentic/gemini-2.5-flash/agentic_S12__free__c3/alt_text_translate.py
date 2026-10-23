import os
from google.cloud import translate_v2 as translate
from vision_models import TranslatedDescriptionResult

def translate_text(text: str, target_language: str = "es") -> TranslatedDescriptionResult:
    """Translates text into the target language using Google Cloud Translation API."""
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return TranslatedDescriptionResult(
        original_description=text,
        translated_description=result['translatedText'],
        target_language=target_language
    )

if __name__ == '__main__':
    # Example usage for demonstration
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or configure authentication.
    original_desc = "A beautiful sunset over the mountains."
    target_lang = "fr"

    print(f"Translating \"{original_desc}\" to {target_lang}...")
    try:
        translation_result = translate_text(original_desc, target_lang)
        print(f"Original: {translation_result.original_description}")
        print(f"Translated ({translation_result.target_language}): {translation_result.translated_description}")
    except Exception as e:
        print(f"Error translating text: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set for Cloud Translation API.")
