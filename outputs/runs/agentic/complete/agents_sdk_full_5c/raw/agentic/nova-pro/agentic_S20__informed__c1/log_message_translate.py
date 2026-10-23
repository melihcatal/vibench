import os
import boto3

client = boto3.client('translate', region_name='us-east-1')

response = client.translate_text(
    Text='Sample log message',
    SourceLanguageCode='en',
    TargetLanguageCode='es'
)

print(response['TranslatedText'])