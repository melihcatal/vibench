import boto3

def check_unsafe_content(text):
    client = boto3.client('comprehend')
    result = client.detect_toxic_content(TextSegments=[{'Text': text}])
    return result['ToxicContent']