import os
import boto3

textract_client = boto3.client('textract', region_name=os.getenv('AWS_REGION'))