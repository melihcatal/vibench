import os
import boto3

def get_kms_client():
    return boto3.client('kms', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def get_key_id():
    return os.getenv('KMS_KEY_ID', 'alias/example_key')