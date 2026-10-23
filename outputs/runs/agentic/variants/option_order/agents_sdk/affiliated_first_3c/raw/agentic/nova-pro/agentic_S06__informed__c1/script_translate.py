import os
import boto3

translate_client = boto3.client('translate', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def translate_text(text, source_lang, target_lang):
    response = translate_client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']