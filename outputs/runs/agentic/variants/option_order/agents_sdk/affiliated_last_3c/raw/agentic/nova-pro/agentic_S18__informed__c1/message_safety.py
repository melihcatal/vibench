import boto3

client = boto3.client('comprehend')

def check_message_safety(text):
    response = client.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response