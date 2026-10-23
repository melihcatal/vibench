import boto3

# Configuration for Amazon Rekognition
AWS_REGION = 'us-west-2'

# Helper function to create a Rekognition client
def get_rekognition_client():
    return boto3.client('rekognition', region_name=AWS_REGION)
