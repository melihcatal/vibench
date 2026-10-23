import os
import boto3

client = boto3.client('comprehend')

text = 'This is a secret label.'
response = client.detect_sentiment(Text=text, LanguageCode='en')
print(response)