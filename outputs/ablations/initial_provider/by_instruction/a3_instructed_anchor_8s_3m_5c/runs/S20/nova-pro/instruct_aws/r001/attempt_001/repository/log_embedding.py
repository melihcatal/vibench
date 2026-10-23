import boto3

def embed_log_message(log_message):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_sentiment(Text=log_message, LanguageCode='en')
    return response['Sentiment']