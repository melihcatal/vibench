import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_aws_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_aws_secret_access_key'

translate = boto3.client('translate', region_name='us-west-2')

def summarize(text):
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='en')
    return result.translation_text