import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def translate_text(text, target_language='es'):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.translatedText