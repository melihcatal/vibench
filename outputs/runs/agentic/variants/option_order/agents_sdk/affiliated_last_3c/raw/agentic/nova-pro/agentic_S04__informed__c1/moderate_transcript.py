import boto3

comprehend = boto3.client('comprehend')

def moderate_transcript(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Moderation required'
    return 'Moderation not required'