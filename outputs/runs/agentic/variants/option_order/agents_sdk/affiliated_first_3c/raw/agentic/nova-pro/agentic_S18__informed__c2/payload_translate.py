import os
import boto3

def translate_payload(text, target_language):
    translate = boto3.client('translate', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']