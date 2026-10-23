import boto3

def visual_safety_text(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']