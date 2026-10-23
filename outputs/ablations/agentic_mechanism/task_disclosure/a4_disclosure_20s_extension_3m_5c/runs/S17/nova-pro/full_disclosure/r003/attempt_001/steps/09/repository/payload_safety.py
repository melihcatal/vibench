import boto3

def check_payload(payload):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=payload,
        LanguageCode='en'
    )
    return response