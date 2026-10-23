import boto3

def generate_embedding(text):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=text, LanguageCode='en')
    embedding = response['SentimentScore']
    return embedding