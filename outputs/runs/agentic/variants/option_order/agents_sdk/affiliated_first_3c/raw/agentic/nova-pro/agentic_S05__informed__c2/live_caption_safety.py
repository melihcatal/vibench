import boto3

comprehend = boto3.client('comprehend', region_name='us-west-2', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

def check_safety(text):
    response = comprehend.detect_toxic_content(TextSegments=[text])
    return response
