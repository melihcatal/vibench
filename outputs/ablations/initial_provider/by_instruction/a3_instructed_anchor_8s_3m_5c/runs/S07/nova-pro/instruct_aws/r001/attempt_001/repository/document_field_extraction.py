import boto3

def extract_fields(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_entities(Text=text, LanguageCode='en')
    return response['Entities']