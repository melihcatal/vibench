import os
import boto3

# Configuration for Amazon Comprehend
COMPREHEND_REGION = os.getenv('AWS_REGION', 'us-west-2')

# Client helper utility for Amazon Comprehend
def get_comprehend_client():
    comprehend_client = boto3.client('comprehend', region_name=COMPREHEND_REGION)
    return comprehend_client
