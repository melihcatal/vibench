import boto3

from security_client import get_translate_client

def get_translate_client():
    return boto3.client('translate')

def compliance_note_translate(text, target_language_code):
    translate_client = get_translate_client()
    response = translate_client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language_code)
    return response['TranslatedText']