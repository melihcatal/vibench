import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_aws_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_aws_secret_access_key'

comprehend = boto3.client('comprehend', region_name='us-west-2')

def check_safety(text):
    result = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    return result.ToxicContent