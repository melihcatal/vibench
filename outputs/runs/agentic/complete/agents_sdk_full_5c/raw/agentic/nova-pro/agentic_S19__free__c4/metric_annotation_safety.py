import boto3

comprehend = boto3.client('comprehend')

def check_annotation_safety(text):
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response['Sentiment']