import boto3
from document_client import get_translate_client

client = get_translate_client()

def translate_text(text, source_lang, target_lang):
    response = client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']