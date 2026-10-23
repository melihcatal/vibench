import boto3
import os

def check_corpus_safety(text: str) -> dict:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    client = boto3.client(
        'comprehend',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    response = client.detect_sentiment(Text=text, LanguageCode='en')
    return response
