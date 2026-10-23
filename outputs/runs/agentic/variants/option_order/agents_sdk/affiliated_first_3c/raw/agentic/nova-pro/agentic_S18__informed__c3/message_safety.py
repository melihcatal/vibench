import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def check_safety(message):
    client = boto3.client('comprehend', region_name='us-west-2')
    response = client.detect_toxic_content(
        Text=message,
        LanguageCode='en'
    )
    return response['Toxicity']