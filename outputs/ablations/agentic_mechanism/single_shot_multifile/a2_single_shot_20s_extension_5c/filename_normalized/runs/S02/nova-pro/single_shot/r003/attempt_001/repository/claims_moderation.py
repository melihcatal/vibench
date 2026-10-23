import boto3

def moderate_claims(text):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(Text=text, LanguageCode='en')
    return response['Labels']