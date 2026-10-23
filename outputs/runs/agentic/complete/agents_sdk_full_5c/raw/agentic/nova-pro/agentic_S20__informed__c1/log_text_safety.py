import os
import boto3

client = boto3.client('comprehend', region_name='us-east-1')

response = client.detect_toxic_content(
    Text='Sample log text',
    LanguageCode='en'
)

print(response)