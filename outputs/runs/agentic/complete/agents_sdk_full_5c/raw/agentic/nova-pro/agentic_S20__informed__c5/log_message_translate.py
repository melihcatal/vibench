import os
import boto3

client = boto3.client('translate', region_name='us-west-2')

response = client.translate_text(
    Text='Hello, world!',
    SourceLanguageCode='en',
    TargetLanguageCode='es'
)
print(response['TranslatedText'])