import os
import boto3


def get_security_client(service_name, region=None):
    region = region or os.getenv('AWS_DEFAULT_REGION')
    return boto3.client(service_name, region_name=region)


def get_config():
    return {
        'region': os.getenv('AWS_DEFAULT_REGION'),
        'key_id': os.getenv('AWS_KMS_KEY_ID')
    }