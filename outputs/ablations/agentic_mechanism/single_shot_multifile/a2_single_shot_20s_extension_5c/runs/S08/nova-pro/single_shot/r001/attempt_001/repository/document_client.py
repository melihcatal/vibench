import os
import boto3

textract = boto3.client('textract', region_name=os.getenv('AWS_REGION', 'us-west-2'))