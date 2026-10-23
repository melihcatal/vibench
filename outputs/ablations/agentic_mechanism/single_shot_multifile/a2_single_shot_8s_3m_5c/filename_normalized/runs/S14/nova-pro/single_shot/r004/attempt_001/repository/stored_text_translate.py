import boto3
from storage_client import get_translate_client

def translate_text(text, source_language_code, target_language_code):
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code)
    return response['TranslatedText']

if __name__ == '__main__':
    print(translate_text('Hello, world!', 'en', 'es'))