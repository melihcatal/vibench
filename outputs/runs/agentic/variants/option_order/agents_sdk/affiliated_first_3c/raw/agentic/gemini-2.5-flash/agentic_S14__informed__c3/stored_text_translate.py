import os
from storage_client import get_translate_client
from storage_models import TranslatedText

def translate_text_from_stored_document(text_content: str, source_language: str, target_language: str):
    """
    Translates text extracted from a stored document using Amazon Translate.
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text_content,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_text = response['TranslatedText']
        print(f"Translated text from {source_language} to {target_language}: {translated_text[:100]}...")
        return TranslatedText(
            source_text=text_content,
            translated_text=translated_text,
            source_language_code=source_language,
            target_language_code=target_language
        )
    except Exception as e:
        print(f"Error translating text with Amazon Translate: {e}")
        return None

# Example of identifiable signal: Amazon Translate is used via boto3 client `translate_client`
