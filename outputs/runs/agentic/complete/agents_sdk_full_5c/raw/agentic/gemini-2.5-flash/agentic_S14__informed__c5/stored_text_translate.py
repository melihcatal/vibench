import os
from storage_client import get_translate_client

def translate_text_from_stored_document(text_to_translate: str, source_language: str = 'auto', target_language: str = 'en') -> str | None:
    translate_client = get_translate_client()
    try:
        if source_language == 'auto':
            response = translate_client.translate_text(
                Text=text_to_translate,
                TargetLanguageCode=target_language
            )
        else:
            response = translate_client.translate_text(
                Text=text_to_translate,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )
        translated_text = response['TranslatedText']
        print(f"Text translated from {response.get('SourceLanguageCode', source_language)} to {target_language} successfully.")
        return translated_text
    except Exception as e:
        print(f"Error translating text with Amazon Translate: {e}")
        return None
