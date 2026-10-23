import boto3

comprehend_client = boto3.client('comprehend')

def check_script_safety(text):
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']