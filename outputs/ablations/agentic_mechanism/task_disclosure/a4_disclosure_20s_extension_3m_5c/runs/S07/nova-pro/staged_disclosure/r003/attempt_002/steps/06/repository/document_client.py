import boto3
import os

# Configuration for AWS Textract
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-west-2')

# Initialize the Textract client
textract_client = boto3.client('textract',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

def extract_text_from_document(document_path):
    """Helper function to extract text from a document using Amazon Textract"""
    with open(document_path, 'rb') as document:
        image_bytes = document.read()

    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '

    return text