import boto3

def moderate_claims(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Claim rejected due to negative sentiment'
    else:
        return 'Claim accepted'