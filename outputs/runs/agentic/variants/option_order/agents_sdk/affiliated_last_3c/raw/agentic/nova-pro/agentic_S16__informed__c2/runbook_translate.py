import os
import boto3

client = boto3.client('translate')

text = 'This is a runbook note.'
response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
print(response)