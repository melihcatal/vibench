import boto3

def summarize_record(record):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=record, LanguageCode='en')
    return response['Sentiment']