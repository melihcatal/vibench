import boto3

def summarize_audit_events():
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text='User logged in successfully.', LanguageCode='en')
    return response['Sentiment']