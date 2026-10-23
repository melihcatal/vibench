import boto3
import json

def translate_result(text, target_language='es'):
    client = boto3.client('translate', region_name='us-east-1')
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']