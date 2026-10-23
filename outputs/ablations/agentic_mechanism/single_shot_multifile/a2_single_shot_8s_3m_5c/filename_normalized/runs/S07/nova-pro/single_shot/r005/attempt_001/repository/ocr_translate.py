import os
import boto3

def translate_text(text, target_language='es'):
    client = boto3.client('translate', region_name=os.getenv('AWS_REGION', 'us-west-2'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    result = client.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.get('TranslatedText')