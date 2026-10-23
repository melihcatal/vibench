import boto3

def archive_summary(transcript):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=transcript, LanguageCode='en')
    return response['Sentiment']