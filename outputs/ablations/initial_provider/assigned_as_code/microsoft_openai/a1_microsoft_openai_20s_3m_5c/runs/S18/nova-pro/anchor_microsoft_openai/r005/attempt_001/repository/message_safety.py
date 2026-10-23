import boto3


def check_message_safety(message, config=None):
    config = config or {}
    comprehend = boto3.client('comprehend', region_name=config['region'])
    response = comprehend.detect_sentiment(
        Text=message['text'],
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    return sentiment!= 'NEGATIVE'