import boto3

def check_safety(text, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('region'))
    response = client.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']