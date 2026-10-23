import boto3

def check_safety(response):
    client = boto3.client('comprehend', region_name='us-west-2')
    text = response['body']['completion']
    result = client.detect_sentiment(Text=text, LanguageCode='en')
    return result['Sentiment']