import os
import boto3

comprehend_client = boto3.client('comprehend', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def check_safety(text):
    response = comprehend_client.detect_toxic_content(TextSegments=[{'Text': text}])
    return response['ResultList'][0]['Toxicity']