import boto3

# Configuration for AWS Comprehend
aws_region = 'us-west-2'

# Initialize the Comprehend client
comprehend_client = boto3.client('comprehend', region_name=aws_region)

def detect_toxic_content(text):
    """Detect toxic content in the given text"""
    response = comprehend_client.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response
