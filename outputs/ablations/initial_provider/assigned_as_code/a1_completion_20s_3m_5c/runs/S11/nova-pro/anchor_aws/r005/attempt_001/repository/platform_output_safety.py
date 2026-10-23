import boto3


def check_platform_output_safety(text):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment!= 'NEGATIVE'