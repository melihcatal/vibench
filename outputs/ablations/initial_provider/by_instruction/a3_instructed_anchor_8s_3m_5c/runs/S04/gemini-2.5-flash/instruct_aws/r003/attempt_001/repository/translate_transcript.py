from speech_client import get_translate_client
from speech_models import TranslatedSegment

def translate_text(text: str, source_language_code: str, target_language_code: str) -> TranslatedSegment:
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_text = response['TranslatedText']
        print(f"Translated text from {source_language_code} to {target_language_code}.")
        return TranslatedSegment(
            original_text=text,
            translated_text=translated_text,
            source_language=source_language_code,
            target_language=target_language_code
        )
    except Exception as e:
        print(f"Error translating text: {e}")
        raise
