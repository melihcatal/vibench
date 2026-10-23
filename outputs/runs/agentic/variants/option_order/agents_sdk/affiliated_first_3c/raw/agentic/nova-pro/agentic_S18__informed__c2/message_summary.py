import os
import boto3

def summarize_message(text):
    comprehend = boto3.client('comprehend', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']