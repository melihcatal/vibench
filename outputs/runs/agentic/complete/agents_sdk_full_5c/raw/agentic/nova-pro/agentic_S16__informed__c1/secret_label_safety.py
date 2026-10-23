import boto3

def check_label_safety(label):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(Text=label, LanguageCode='en')
    return response['ToxicContent']