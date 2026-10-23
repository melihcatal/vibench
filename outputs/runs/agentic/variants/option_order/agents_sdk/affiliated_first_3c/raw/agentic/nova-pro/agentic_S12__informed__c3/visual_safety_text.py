import boto3

comprehend = boto3.client('comprehend')

def check_safety(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    print('Sentiment:', sentiment)