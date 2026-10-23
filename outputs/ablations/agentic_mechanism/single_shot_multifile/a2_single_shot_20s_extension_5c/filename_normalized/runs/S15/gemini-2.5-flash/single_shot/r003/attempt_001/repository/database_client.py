import os
import boto3

def get_dynamodb_client():
    region_name = os.environ.get('AWS_REGION_NAME')
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if not all([region_name, aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS credentials (AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) must be set in environment variables.")

    dynamodb = boto3.client(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    return dynamodb