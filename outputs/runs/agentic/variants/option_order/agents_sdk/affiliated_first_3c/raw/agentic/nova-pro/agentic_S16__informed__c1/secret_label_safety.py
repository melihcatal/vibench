import boto3

def secret_label_safety(secret_name):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(
        Text=secret_name,
        LanguageCode='en'
    )
    return response['Labels']