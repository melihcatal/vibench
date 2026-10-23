import boto3

def check_payload_safety(text):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(Text=text, LanguageCode='en')
    return response['ToxicContent']