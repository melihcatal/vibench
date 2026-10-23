import boto3

def create_comprehend_client():
    comprehend_client = boto3.client('comprehend')
    return comprehend_client

def detect_toxic_content(text):
    client = create_comprehend_client()
    response = client.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response
