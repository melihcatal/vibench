import os
import boto3

# AWS SDK credentials – you can also load from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def get_textract_client():
    """Create and return a boto3 Textract client configured with credentials."""
    return boto3.client(
        'textract',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )