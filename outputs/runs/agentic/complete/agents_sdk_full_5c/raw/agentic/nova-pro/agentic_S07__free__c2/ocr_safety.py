import boto3
from document_client import get_comprehend_client

client = get_comprehend_client()

def check_safety(text):
    response = client.detect_toxic_content(TextSegments=[{'Text': text}])
    return response['ToxicContent']