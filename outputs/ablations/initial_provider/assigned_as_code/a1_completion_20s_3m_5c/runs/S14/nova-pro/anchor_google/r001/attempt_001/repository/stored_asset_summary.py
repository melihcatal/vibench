import boto3

def summarize_text(text):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response['Sentiment']