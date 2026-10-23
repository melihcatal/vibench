import boto3

def check_annotation_safety(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']!= 'NEGATIVE'