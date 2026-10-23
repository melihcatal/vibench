import boto3

comprehend = boto3.client('comprehend', region_name='us-east-1')

def embed_text(text):
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response.get('Sentiment')