import boto3

comprehend = boto3.client('comprehend')

def summarize_message(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response