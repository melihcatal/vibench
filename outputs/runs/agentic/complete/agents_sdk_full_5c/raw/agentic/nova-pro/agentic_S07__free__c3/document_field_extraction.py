import boto3

def extract_fields(text):
    client = boto3.client('comprehend')
    response = client.detect_entities(Text=text, LanguageCode='en')
    return response['Entities']