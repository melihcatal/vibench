import boto3

comprehend = boto3.client('comprehend')

def check_safety(text):
    response = comprehend.detect_toxic_content(TextSegments=[{'Text': text}])
    return response