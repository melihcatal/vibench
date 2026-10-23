import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def translate_payload(message):
    client = boto3.client('translate', region_name='us-west-2')
    response = client.translate_text(
        Text=message,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )
    return response['TranslatedText']