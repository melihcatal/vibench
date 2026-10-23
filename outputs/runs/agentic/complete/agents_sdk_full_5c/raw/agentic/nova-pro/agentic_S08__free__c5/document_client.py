import os
import boto3

def get_textract_client():
    return boto3.client('textract', region_name=os.getenv('AWS_REGION'))