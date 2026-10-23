import boto3


def check_script_safety(script):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=script, LanguageCode='en')
    return response['Sentiment']