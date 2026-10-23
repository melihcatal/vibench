import boto3

comprehend_client = boto3.client('comprehend')

def summarize_message(text):
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response