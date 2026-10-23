import boto3
import json

def check_prompt_safety(prompt):
    client = boto3.client('comprehend', region_name='us-east-1')
    response = client.detect_sentiment(Text=prompt, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment!= 'NEGATIVE'