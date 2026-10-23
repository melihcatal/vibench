import boto3

def check_payload(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response
