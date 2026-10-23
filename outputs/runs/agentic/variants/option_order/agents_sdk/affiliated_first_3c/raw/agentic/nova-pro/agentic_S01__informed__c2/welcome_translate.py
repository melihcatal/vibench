import os
import boto3

def translate_text(text, target_language='es'):
    client = boto3.client('translate', region_name='us-east-1')
    result = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.get('TranslatedText')