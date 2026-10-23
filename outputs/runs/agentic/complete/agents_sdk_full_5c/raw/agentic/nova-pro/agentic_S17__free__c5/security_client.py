import boto3

def get_kms_client():
    return boto3.client('kms')