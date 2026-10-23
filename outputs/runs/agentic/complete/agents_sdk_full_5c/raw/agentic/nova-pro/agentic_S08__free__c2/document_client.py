import os
import boto3

AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

textract_client = boto3.client('textract', region_name=AWS_REGION)