import boto3
from [HELPER] document_client import get_translate_client

def translate_text(text, source_lang='en', target_lang='es'):
    client = get_translate_client()
    response = client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']