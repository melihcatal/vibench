import boto3
from botocore.exceptions import NoCredentialsError

def embed_text(text):
    client = boto3.client('comprehend')
    try:
        result = client.detect_sentiment(Text=text, LanguageCode='en')
        return result['Sentiment']
    except NoCredentialsError:
        raise Exception('AWS credentials not found')