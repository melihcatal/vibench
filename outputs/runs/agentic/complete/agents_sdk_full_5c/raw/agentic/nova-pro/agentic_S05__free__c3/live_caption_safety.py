import boto3

comprehend = boto3.client('comprehend', region_name='us-west-2')

def check_safety(caption):
    response = comprehend.detect_sentiment(Text=caption, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return False
    return True