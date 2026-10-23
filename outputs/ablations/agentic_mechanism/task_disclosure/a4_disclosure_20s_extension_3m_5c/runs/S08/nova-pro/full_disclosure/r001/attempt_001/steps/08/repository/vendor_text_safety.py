import boto3
import os

# Set up the Amazon Comprehend client
comprehend = boto3.client('comprehend', region_name='us-east-1',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def moderate_text(text):
    """Moderates the given text using Amazon Comprehend."""
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    if response['Labels']:
        return True
    else:
        return False