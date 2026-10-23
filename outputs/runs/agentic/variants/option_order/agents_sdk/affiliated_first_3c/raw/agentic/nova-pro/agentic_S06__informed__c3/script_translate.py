import os
import boto3

translate_client = boto3.client('translate', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def translate_script(text, source_language_code='en', target_language_code='es'):
    result = translate_client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result['TranslatedText']