import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def safety_threshold(text):
    comprehend = boto3.client('comprehend', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']!= 'NEGATIVE'