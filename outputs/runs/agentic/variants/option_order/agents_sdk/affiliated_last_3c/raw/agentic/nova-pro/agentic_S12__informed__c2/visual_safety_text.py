import boto3

def check_safety(text):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(Text=text)
    return response['ToxicContent']