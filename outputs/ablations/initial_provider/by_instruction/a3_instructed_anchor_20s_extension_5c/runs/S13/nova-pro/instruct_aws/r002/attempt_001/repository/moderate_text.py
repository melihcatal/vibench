import boto3

comprehend = boto3.client('comprehend')

def moderate_text(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response
