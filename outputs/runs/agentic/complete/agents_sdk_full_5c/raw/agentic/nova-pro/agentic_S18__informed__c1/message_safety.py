import boto3

def message_safety(message):
    comprehend_client = boto3.client('comprehend', region_name='us-west-2')
    response = comprehend_client.detect_sentiment(
        Text=message,
        LanguageCode='en'
    )
    return response['Sentiment']