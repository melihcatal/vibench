import os
import boto3

def check_safety(text):
    client = boto3.client('comprehend', region_name=os.getenv('AWS_REGION', 'us-west-2'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = client.detect_toxic_content(TextSegments=[{'Text': text}])
    return response['Results'][0]['Toxicity']