import boto3

comprehend_client = boto3.client('comprehend')

def check_unsafe_content(text):
    response = comprehend_client.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response