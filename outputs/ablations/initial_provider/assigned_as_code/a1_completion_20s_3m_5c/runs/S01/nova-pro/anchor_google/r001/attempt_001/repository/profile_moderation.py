import boto3


def moderate_text(text):
    comprehend = boto3.client('comprehend')
    result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return result.get('Sentiment')