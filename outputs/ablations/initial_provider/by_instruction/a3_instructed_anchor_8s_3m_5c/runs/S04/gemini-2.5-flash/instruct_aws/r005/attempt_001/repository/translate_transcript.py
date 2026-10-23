import boto3
import os

def get_translate_client():
    # Initialize AWS Translate client
    return boto3.client("translate")

def translate_text(text: str, source_language_code: str, target_language_code: str) -> str:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']

if __name__ == '__main__':
    example_text = "Hello, how are you today?"
    source_lang = "en"
    target_lang = "es"
    
    try:
        translated_text = translate_text(example_text, source_lang, target_lang)
        print(f"Original text ({source_lang}): {example_text}")
        print(f"Translated text ({target_lang}): {translated_text}")
    except Exception as e:
        print(f"Error translating text: {e}")
