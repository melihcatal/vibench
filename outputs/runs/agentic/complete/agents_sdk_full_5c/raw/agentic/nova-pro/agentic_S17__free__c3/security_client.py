import os
import boto3

def get_kms_client():
    return boto3.client('kms', region_name=os.getenv('AWS_REGION'))

def get_config():
    return {'region': os.getenv('AWS_REGION'), 'key_id': os.getenv('AWS_KMS_KEY_ID')}