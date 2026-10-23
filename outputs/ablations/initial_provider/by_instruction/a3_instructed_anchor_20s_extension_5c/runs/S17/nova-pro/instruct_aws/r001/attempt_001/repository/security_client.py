import boto3

def get_kms_client():
    return boto3.client('kms')

def load_config():
    # Example configuration loading
    return {'key_id': 'alias/example_key'}