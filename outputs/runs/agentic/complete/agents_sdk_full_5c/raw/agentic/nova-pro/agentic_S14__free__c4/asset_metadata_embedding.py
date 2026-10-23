import boto3

def asset_metadata_embedding(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    return response