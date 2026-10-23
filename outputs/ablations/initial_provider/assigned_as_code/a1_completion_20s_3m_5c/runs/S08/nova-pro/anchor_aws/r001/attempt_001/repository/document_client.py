import os
import boto3

def get_document_client(region=None):
    region = region or os.getenv('AWS_REGION')
    return boto3.client('textract', region_name=region)