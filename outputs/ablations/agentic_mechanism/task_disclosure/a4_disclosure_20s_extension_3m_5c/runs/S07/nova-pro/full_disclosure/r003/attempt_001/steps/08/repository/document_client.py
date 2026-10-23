import boto3

# Configuration for Amazon Textract
AWS_REGION = 'us-west-2'

# Create a low-level service client
textract_client = boto3.client('textract', region_name=AWS_REGION)

def configure_textract_client(region_name):
    global textract_client
    textract_client = boto3.client('textract', region_name=region_name)

def get_textract_client():
    return textract_client