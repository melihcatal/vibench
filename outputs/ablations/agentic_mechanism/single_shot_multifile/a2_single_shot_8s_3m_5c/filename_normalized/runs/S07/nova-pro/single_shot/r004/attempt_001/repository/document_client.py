import os
import boto3

def get_textract_client():
    return boto3.client('textract', region_name=os.getenv('AWS_REGION', 'us-west-2'))

def get_translate_client():
    return boto3.client('translate', region_name=os.getenv('AWS_REGION', 'us-west-2'))