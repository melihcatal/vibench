import boto3

def moderate_claims(text):
    comprehend = boto3.client('comprehend')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return sentiment['Sentiment']